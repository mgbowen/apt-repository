# apt-repository

To install packages from this repository:

### Debian bullseye

```
wget https://apt.mgbowen.dev/mgbowen-apt-repository.asc | sudo apt-key add -
echo 'deb https://apt.mgbowen.dev/debian/ bullseye windows-fido-bridge' \
    | sudo tee /etc/apt/sources.list.d/mgbowen.list
sudo apt update
```
