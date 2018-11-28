## sh myBash.sh '192.168.1.100' 'gramatica.txt'
ip_dir=$1
remote_file=$3
local_file=$2

ftp -n ${ip_dir} <<END_SCRIPT
user rcp rcp
get ${remote_file} ${local_file} 

quit
END_SCRIPT
exit 0
