# Creating the package

To create the debian package use the following steps

```bash
cmake -B"./build" \
      -DCMAKE_INSTALL_PREFIX="/usr" \
      -DCMAKE_BUILD_TYPE=Release
cd build
cpack -G DEB
```
