while true do
  system 'scrot /tmp/tsc.jpg'
  system 'scp /tmp/tsc.jpg 106.186.22.139:~/plib/workspace/'
  sleep 60*5
end

