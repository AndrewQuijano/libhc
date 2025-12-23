# Libhc
Use this header inconjuction with [PIRATE](https://github.com/panda-re/panda/blob/dev/panda/plugins/taint2/PIRATE.md) for making your hypercalls. For an example, see how [LAVA](https://github.com/panda-re/lava/blob/master/tools/include/pirate_mark_lava.h) and [PANDA](https://github.com/panda-re/panda/blob/dev/panda/plugins/pri_taint/pri_taint.cpp) use this library for an architecture neutral hypercall system to taint bytes for injecting bugs in code.

This has the advantage of once you get this working in one platform, it is much easier to make your plug-in work in other archtictures.

##  Creating the package locally
To create the debian package use the following steps, the package would be under the `build` folder.

```bash
cmake -B"./build" \
      -DCMAKE_INSTALL_PREFIX="/usr" \
      -DCMAKE_BUILD_TYPE=Release
pushd build
cpack -G DEB
popd
```
