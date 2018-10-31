file_hash=`curl -F 'file=@./file1.txt' 127.0.0.1:5000/upload`
echo ${file_hash}

