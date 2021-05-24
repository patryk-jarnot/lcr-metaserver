SCRIPTPATH="$( cd "$(dirname "$0")" ; pwd -P )"

echo $SCRIPTPATH
cd $SCRIPTPATH/..

if ! screen -list | grep -q "server"; then
  cd platolocoui/
  screen -dmS server npm start
fi
