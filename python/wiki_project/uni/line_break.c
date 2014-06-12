#include<stdio.h>
#include<string.h>

int main(int argc,char *argv[])
{
	FILE* stream;
	char * html = "/html>";
	const int len = strlen(html);
	int cursor = 0;
	char buf[2];
	buf[1] = '\0';
	int c = 0;
	long long read = 0;
	if((stream=fopen(argv[1],"r"))==NULL){
		fprintf(stderr,"Can not open output file.\n");
		return 0;
	}
	while(1){
		int ret = fread(buf,1, 1,stream);
		read += ret;
		if (ret != 1){
			break;
		}
		//printf("%c",buf[0]);
		if (buf[0] == html[cursor]){
			cursor++;
		}else{
			cursor = 0;
		}
		if (buf[0] == '\n'){
			printf ("^^\n");
		}
		if (cursor == 6){
			cursor = 0;
			printf("%d,Reading...%lld\n", c, read);
			c++;
		}
	}
	fclose(stream);
	return 0;
}




