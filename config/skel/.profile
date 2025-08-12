# ~/.profile - default profile for pubnix
[ -r /etc/profile ] && . /etc/profile
# Ensure ~/bin is on PATH
case :$PATH: in
  *:$HOME/bin:*) ;;
  *) PATH="$HOME/bin:$PATH" ;;
esac
