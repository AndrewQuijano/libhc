import argparse
from pathlib import Path
import shlex
import shutil
import subprocess
import sys
import tempfile


def run_hypercall_test(architecture: str, ci: bool = False):
    """Require a hypercall during recording and again in a fresh replay process."""
    binary = Path(__file__).resolve().parent / f"test_hc_{architecture}"
    if not binary.is_file():
        raise FileNotFoundError(
            f"Missing {binary}. Build the libhc test with -DARCH={architecture} first."
        )
    with tempfile.TemporaryDirectory(prefix="libhc-test-") as directory:
        for phase in ("record", "replay"):
            command = [sys.executable, str(Path(__file__).resolve()),
                       "--arch", architecture, "--phase", phase,
                       "--work", directory]
            if ci:
                command.append("--ci")
            subprocess.run(command, check=True, timeout=240)
    print(f"[PyPANDA TEST] PASS: {architecture} copy, record, and replay hypercalls")


def run_phase(architecture: str, phase: str, work: Path, ci: bool):
    from pandare import Panda

    expected = [6767, 42, 43, 44, 45]
    observed = []
    panda = Panda(generic=architecture)
    recording = str(work / "recording")

    @panda.hypercall(expected[0])
    def before_hc(cpu):
        values = [panda.arch.get_arg(cpu, i, convention="syscall")
                  for i in range(len(expected))]
        assert values == expected, f"Expected {expected}, got {values}"
        observed.append(values)
        print(f"[PyPANDA TEST] {phase}: hypercall intercepted: {values}", flush=True)
        if len(observed) > 1:
            raise AssertionError("Expected exactly one hypercall")

    if ci:
        panda.set_complete_rr_snapshot()

    if phase == "record":
        binary = Path(__file__).resolve().parent / f"test_hc_{architecture}"
        payload = work / "hc_payload"
        payload.mkdir()
        shutil.copy2(binary, payload / binary.name)

        @panda.queue_blocking
        def record():
            panda.revert_sync("root")
            panda.copy_to_guest(str(payload), iso_name=str(work / "payload.iso"))
            program = shlex.quote(f"./{payload.name}/{binary.name}")
            panda.type_serial_cmd(program + "; printf 'LIBHC_EXIT=%s\\n' \"$?\"")
            panda.run_monitor_cmd("begin_record " + recording)
            try:
                output = panda.finish_serial_cmd(timeout=90)
            finally:
                panda.run_monitor_cmd("end_record")
            print(output, flush=True)
            assert "LIBHC_EXIT=0" in output and "[+] Success!" in output, output
            assert observed == [expected], f"No matching recording hypercall: {observed}"
            panda.end_analysis()

        panda.run()
    else:
        panda.run_replay(recording)

    assert not panda.was_aborted(), f"PANDA aborted during {phase}"
    assert observed == [expected], f"No matching {phase} hypercall: {observed}"
    print(f"[PyPANDA TEST] PASS: {phase}", flush=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Test libhc copy and record/replay hypercalls")
    parser.add_argument("-a", "--arch", "--architecture",
                        choices=["i386", "x86_64", "arm", "aarch64"],
                        default="x86_64", dest="architecture")
    parser.add_argument("--ci", action="store_true",
                        help="Use complete RR snapshots")
    parser.add_argument("--phase", choices=["record", "replay"], help=argparse.SUPPRESS)
    parser.add_argument("--work", type=Path, help=argparse.SUPPRESS)
    args = parser.parse_args()
    if args.phase:
        if args.work is None:
            parser.error("--phase requires --work")
        run_phase(args.architecture, args.phase, args.work, args.ci)
    else:
        run_hypercall_test(args.architecture, args.ci)
