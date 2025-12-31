#include <stdio.h>
#include "hypercall.h"


int main() {
    printf("[*] Attempting hypercall 6767...\n");
    printf("[!] NOTE: This will FAIL if run outside of PANDA/QEMU!\n");
    int magic = 6767;

    // In PANDA, the handler will set the return value to 6767 if successful
    int result = (int) igloo_hypercall4(magic, 42, 43, 44, 45);

    printf("[+] Hypercall finished. Result: %d\n", result);

    if (result == magic) {
        printf("[+] Success!\n");
        return 0;
    } else {
        printf("[-] Failure: Expected 6767, got %d\n", result);
        return 1;
    }
}