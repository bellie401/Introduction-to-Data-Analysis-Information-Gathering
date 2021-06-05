#!/bin/bash
synonymNumbers=(1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20) #Change this
ValSpacing=1 #this (refers to spacing in synonymNumbers)
RunOriginal=0 #this
RunTitles=1 #this
RunDescs=0 #this
RunNarrs=0 #this

cd ..
cd Downloads
cd IR-2019-2020-Project-1
echo "PRE-PROCESSING & RUN QUERIES"
for i in ${synonymNumbers[*]}
do
	python qGen.py $i t #and this if needed
	if [ $RunTitles -eq 1 ];
	then
	IndriRunQuery title_aug^$i.queries > results/result_title_aug^$i.trec
	fi
	if [ $RunDescs -eq 1 ];
	then
	IndriRunQuery title+desc_aug^$i.queries > results/result_title+desc_aug^$i.trec
	fi
	if [ $RunNarrs -eq 1 ];
	then
	IndriRunQuery title+desc+narr_aug^$i.queries > results/result_title+desc+narr_aug^$i.trec
	fi
done
if [ $RunOriginal -eq 1 ];
then
echo "Running Stock Queries"
IndriRunQuery IndriRunQuery.queries.file.301-450-titles-only.EXAMPLE > results/result_baseline_titles.trec
IndriRunQuery title.queries > results/result_titles_v1.trec
IndriRunQuery title+desc.queries > results/result_titles_desc_v1.trec
IndriRunQuery title+desc+narr.queries > results/result_titles_desc_narr_v1.trec
fi

echo "TREC_EVAL"
cd ../trec_eval-9.0.7/
tempno=$((${synonymNumbers[0]}-$ValSpacing)) #Needed for first blank .csv file

echo "QUERIES 301-350"
#Evaluate results w/out synonyms
./trec_eval  ../IR-2019-2020-Project-1/qrels.301-350.trec6.adhoc ../IR-2019-2020-Project-1/results/result_baseline_titles.trec > temp1
./trec_eval  ../IR-2019-2020-Project-1/qrels.301-350.trec6.adhoc ../IR-2019-2020-Project-1/results/result_titles_v1.trec >temp2
./trec_eval  ../IR-2019-2020-Project-1/qrels.301-350.trec6.adhoc ../IR-2019-2020-Project-1/results/result_titles_desc_v1.trec >temp7
./trec_eval  ../IR-2019-2020-Project-1/qrels.301-350.trec6.adhoc ../IR-2019-2020-Project-1/results/result_titles_desc_narr_v1.trec >temp8

#Create blank .csv files
>results/data_t_301-350_$tempno.csv
>results/data_d_301-350_$tempno.csv
>results/data_n_301-350_$tempno.csv
for i in ${synonymNumbers[*]}
do
	echo "$i Synonyms "
	#Evaluate and save results
	./trec_eval  ../IR-2019-2020-Project-1/qrels.301-350.trec6.adhoc ../IR-2019-2020-Project-1/results/result_title_aug^$i.trec >temp4
	./trec_eval  ../IR-2019-2020-Project-1/qrels.301-350.trec6.adhoc ../IR-2019-2020-Project-1/results/result_title+desc_aug^$i.trec >temp5
	./trec_eval  ../IR-2019-2020-Project-1/qrels.301-350.trec6.adhoc ../IR-2019-2020-Project-1/results/result_title+desc+narr_aug^$i.trec >temp6
	#Only keep the 3rd column with the values
	 awk '{print $3}' temp4 > results/data_t_$i
	 awk '{print $3}' temp5 > results/data_d_$i
	 awk '{print $3}' temp6 > results/data_n_$i
	num=$(($i-$ValSpacing))
	#Paste these values along with the previous in a new file
	paste results/data_t_301-350_$num.csv results/data_t_$i > results/data_t_301-350_$i.csv
	paste results/data_d_301-350_$num.csv results/data_d_$i > results/data_d_301-350_$i.csv
	paste results/data_n_301-350_$num.csv results/data_n_$i > results/data_n_301-350_$i.csv
	#Print only P5, P10 etc
	echo "Title"
	sed '1,21d' ./temp4 
	echo "Title+Desc"
	sed '1,21d' ./temp5 
	echo "Title+Desc+Narr"
	sed '1,21d' ./temp6 
done
#Print stock results
echo "Stock"
sed '1,21d' ./temp1 >trim1
sed '1,21d' ./temp2 >trim2
echo "Titles"
sdiff trim1 trim2
echo "Title+Desc"
sed '1,21d' ./temp7
echo "Title+Desc+Narr"
sed '1,21d' ./temp8

#Rinse and repeat..

echo "QUERIES 351-400"
./trec_eval  ../IR-2019-2020-Project-1/qrels.351-400.trec7.adhoc ../IR-2019-2020-Project-1/results/result_baseline_titles.trec > temp1 
./trec_eval  ../IR-2019-2020-Project-1/qrels.351-400.trec7.adhoc ../IR-2019-2020-Project-1/results/result_titles_v1.trec >temp2 
./trec_eval  ../IR-2019-2020-Project-1/qrels.351-400.trec7.adhoc ../IR-2019-2020-Project-1/results/result_titles_desc_v1.trec >temp7
./trec_eval  ../IR-2019-2020-Project-1/qrels.351-400.trec7.adhoc ../IR-2019-2020-Project-1/results/result_titles_desc_narr_v1.trec >temp8

>results/data_t_351-400_$tempno.csv
>results/data_d_351-400_$tempno.csv
>results/data_n_351-400_$tempno.csv
for i in ${synonymNumbers[*]}
do
	echo "$i Synonyms "
	./trec_eval  ../IR-2019-2020-Project-1/qrels.351-400.trec7.adhoc ../IR-2019-2020-Project-1/results/result_title_aug^$i.trec >temp4
	./trec_eval  ../IR-2019-2020-Project-1/qrels.351-400.trec7.adhoc ../IR-2019-2020-Project-1/results/result_title+desc_aug^$i.trec >temp5
	./trec_eval  ../IR-2019-2020-Project-1/qrels.351-400.trec7.adhoc ../IR-2019-2020-Project-1/results/result_title+desc+narr_aug^$i.trec >temp6
	 awk '{print $3}' temp4 > results/data_t_$i
	 awk '{print $3}' temp5 > results/data_d_$i
	 awk '{print $3}' temp6 > results/data_n_$i
	num=$(($i-$ValSpacing))
	paste results/data_t_351-400_$num.csv results/data_t_$i > results/data_t_351-400_$i.csv
	paste results/data_d_351-400_$num.csv results/data_d_$i > results/data_d_351-400_$i.csv
	paste results/data_n_351-400_$num.csv results/data_n_$i > results/data_n_351-400_$i.csv
	echo "Title"
	sed '1,21d' ./temp4 
	echo "Title+Desc"
	sed '1,21d' ./temp5 
	echo "Title+Desc+Narr"
	sed '1,21d' ./temp6 
done
echo "Stock"
sed '1,21d' ./temp1 >trim1
sed '1,21d' ./temp2 >trim2
echo "Titles"
sdiff trim1 trim2
echo "Title+Desc"
sed '1,21d' ./temp7
echo "Title+Desc+Narr"
sed '1,21d' ./temp8



echo "QUERIES 401-450"
./trec_eval  ../IR-2019-2020-Project-1/qrels.401-450.trec8.adhoc ../IR-2019-2020-Project-1/results/result_baseline_titles.trec > temp1 
./trec_eval  ../IR-2019-2020-Project-1/qrels.401-450.trec8.adhoc ../IR-2019-2020-Project-1/results/result_titles_v1.trec >temp2 
./trec_eval  ../IR-2019-2020-Project-1/qrels.401-450.trec8.adhoc ../IR-2019-2020-Project-1/results/result_titles_desc_v1.trec >temp7
./trec_eval  ../IR-2019-2020-Project-1/qrels.401-450.trec8.adhoc ../IR-2019-2020-Project-1/results/result_titles_desc_narr_v1.trec >temp8

>results/data_t_401-450_$tempno.csv
>results/data_d_401-450_$tempno.csv
>results/data_n_401-450_$tempno.csv
for i in ${synonymNumbers[*]}
do
	echo "$i Synonyms "
	./trec_eval  ../IR-2019-2020-Project-1/qrels.401-450.trec8.adhoc ../IR-2019-2020-Project-1/results/result_title_aug^$i.trec >temp4
	./trec_eval  ../IR-2019-2020-Project-1/qrels.401-450.trec8.adhoc ../IR-2019-2020-Project-1/results/result_title+desc_aug^$i.trec >temp5
	./trec_eval  ../IR-2019-2020-Project-1/qrels.401-450.trec8.adhoc ../IR-2019-2020-Project-1/results/result_title+desc+narr_aug^$i.trec >temp6
	 awk '{print $3}' temp4 > results/data_t_$i
	 awk '{print $3}' temp5 > results/data_d_$i
	 awk '{print $3}' temp6 > results/data_n_$i
	num=$(($i-$ValSpacing))
	paste results/data_t_401-450_$num.csv results/data_t_$i > results/data_t_401-450_$i.csv
	paste results/data_d_401-450_$num.csv results/data_d_$i > results/data_d_401-450_$i.csv
	paste results/data_n_401-450_$num.csv results/data_n_$i > results/data_n_401-450_$i.csv
	echo "Title"
	sed '1,21d' ./temp4 
	echo "Title+Desc"
	sed '1,21d' ./temp5 
	echo "Title+Desc+Narr"
	sed '1,21d' ./temp6 
done
echo "Stock"
sed '1,21d' ./temp1 >trim1
sed '1,21d' ./temp2 >trim2
echo "Titles"
sdiff trim1 trim2
echo "Title+Desc"
sed '1,21d' ./temp7
echo "Title+Desc+Narr"
sed '1,21d' ./temp8



