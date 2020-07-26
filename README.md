# apt-repository

Source code for this repository is [on GitHub](https://github.com/mgbowen/apt-repository).

### Debian bullseye

```
sudo apt install apt-transport-https ca-certificates curl gpg

curl https://apt.mgbowen.dev/mgbowen-apt-repository.asc | sudo apt-key add -
echo 'deb https://apt.mgbowen.dev/debian/ bullseye main' \
    | sudo tee /etc/apt/sources.list.d/mgbowen.list > /dev/null
sudo apt update
```
