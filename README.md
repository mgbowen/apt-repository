# apt-repository

To install packages from this repository:

### Debian bullseye

```
sudo apt install apt-transport-https ca-certificates curl

curl https://apt.mgbowen.dev/mgbowen-apt-repository.asc | sudo apt-key add -
echo 'deb https://apt.mgbowen.dev/debian/ bullseye windows-fido-bridge' \
    | sudo tee /etc/apt/sources.list.d/mgbowen.list > /dev/null
sudo apt update
```
