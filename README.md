## Usage:
```
$ python cxxheader.py -o protobuf.h -n google proto stuff
```

Outputs a file called `protobuf.h` with the following contents:

```c++
#ifndef _GOOGLE_PROTO_STUFF_PROTOBUF_H_
#define _GOOGLE_PROTO_STUFF_PROTOBUF_H_

namespace google {
namespace proto {
namespace stuff {



} // namespace stuff
} // namespace proto
} // namespace google

#endif _GOOGLE_PROTO_STUFF_PROTOBUF_H_

```
