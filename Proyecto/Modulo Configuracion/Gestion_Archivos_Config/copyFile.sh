## sh myBash.sh '192.168.1.100' 'gramatica.txt'
ip_dir=$1
dir_original=$2
dir_destino=$3
remote_user=$4
remote_password=$5
#las direcciones ya incluyen os nombres de archivo

{
echo open ${ip_dir}
sleep 1
echo ${remote_user}
sleep 1
echo ${remote_password}
sleep 1
echo en
sleep 1
echo conf
sleep 1
echo copy ${dir_original} ${dir_destino} #COPY es de RCP100
sleep 1
echo dir
sleep 1
echo exit
} | telnet 


#telnet ${ip_dir} <<!
#jonathanoleaz 
#Samsung4660 
#echo ${ip_dir}
#cp ${dir_original} ${dir_destino} 
#exit
#fin
