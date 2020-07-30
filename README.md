# apt-repository

Source code for this repository is [on GitHub](https://github.com/mgbowen/apt-repository).

### Debian bullseye

```
sudo apt install apt-transport-https ca-certificates curl gpg

sudo apt-key adv --keyserver keys.openpgp.org --recv-keys 59E68EAC9C749457
echo 'deb https://apt.mgbowen.dev/debian/ bullseye main' \
    | sudo tee /etc/apt/sources.list.d/mgbowen.list > /dev/null
sudo apt update
```
