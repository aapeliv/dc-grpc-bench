#!/bin/sh

# generate API protos and grpc stuff
find . -name '*.proto' | protoc -I. \
  --plugin=protoc-gen-grpc_python=$(which grpc_python_plugin) \
  \
  --python_out=. \
  --grpc_python_out=. \
  \
  $(xargs)

echo "OK"
