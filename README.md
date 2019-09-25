# INT_WEB
# Build Image:
docker build -t intweb:$tag .
# Run container
docker run -it -p 5000:5000 intweb:$tag
