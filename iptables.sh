#!/bin/sh
##
#################################################
### Write by wzk with iptables for background ###
### This scricpt for get bytes for each host  ###
#################################################
## $Id$ #

PATH=/sbin:/bin:/usr/sbin:/usr/bin:/usr/local/sbin:/usr/local/bin
export PATH

TMP_DIR=/tmp
TMP_FILE=all_bytes_iptables
TMP_SQL=all_sql_file_iptables

IPTABLES=iptables
IPTABLES_OPTIONS="-L ${1} -n -x -v "
GREP=grep
SED=sed
TR=tr
CAT=cat
CUT=cut

cd ${TMP_DIR}
${IPTABLES} ${IPTABLES_OPTIONS} | ${TR} -s ' ' | ${SED} -e 's/^ //' \
| ${GREP} "^[0-9]" | ${CUT} -d' ' -f2,8,9 > ${TMP_FILE}

#
# Bytes for output
#
#${CAT} ${TMP_FILE}
#echo "/tmp/temp.txt"
${CAT} ${TMP_FILE} | ${CUT} -d' ' -f1,2 | ${GREP} -v "0.0.0.0/0" >/tmp/temp1.txt 
${CAT} ${TMP_FILE} | ${CUT} -d' ' -f1,2,3 | ${GREP}  "0.0.0.0/0 0.0.0.0/0"|${CUT} -d' ' -f1 >/tmp/temp5.txt 

#
# Bytes for input
#
#echo "Start for INPUT"
${CAT} ${TMP_FILE} | ${CUT} -d' ' -f1,3 | ${GREP} -v "0.0.0.0/0" >/tmp/temp2.txt 
cat /tmp/temp1.txt | while read LINE
do 
   echo $LINE | cut -d' ' -f1 | bc >/tmp/temp3.txt
done
cat /tmp/temp2.txt | while read LINE
do 
   echo $LINE | cut -d' ' -f1 | bc >/tmp/temp4.txt
done
echo "" >/srv/http/iptables/index.html
echo "<head><meta http-equiv=\"Content-Type\" content=\"text/html; charset=utf-8\"></head>" >>/srv/http/iptables/index.html
echo "<p>统计时间：    " >>/srv/http/iptables/index.html
date   >>/srv/http/iptables/index.html
echo "</br>" >>/srv/http/iptables/index.html
echo "流入内网的流量： " >>/srv/http/iptables/index.html
cat /tmp/temp3.txt >>/srv/http/iptables/index.html
echo "</br>" >>/srv/http/iptables/index.html
echo "流出内网的流量： " >>/srv/http/iptables/index.html
cat /tmp/temp4.txt >>/srv/http/iptables/index.html
echo "</br>" >>/srv/http/iptables/index.html
echo "外网流入流量： " >>/srv/http/iptables/index.html
head -n 1 /tmp/temp5.txt >> /srv/http/iptables/index.html
echo "</br>" >>/srv/http/iptables/index.html
echo "流出外网的流量： " >>/srv/http/iptables/index.html
tail -n 1 /tmp/temp5.txt >> /srv/http/iptables/index.html
echo "</p>" >>/srv/http/iptables/index.html
