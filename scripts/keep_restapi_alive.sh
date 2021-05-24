SCRIPTPATH="$( cd "$(dirname "$0")" ; pwd -P )"

echo $SCRIPTPATH
cd $SCRIPTPATH/..
source init.sh

if ! screen -list | grep -q "restapi"; then
	cd platolocorestapi/src
	export PATH=$PATH:/home/pjarnot/bin
  screen -dmS restapi python3 __main__.py
fi
