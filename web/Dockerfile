FROM tomcat

ENV RESERVED_MEGABYTES 256

COPY entrypoint.sh /entrypoint.sh

RUN rm -rf /usr/local/tomcat/webapps/manager
RUN rm -rf /usr/local/tomcat/webapps/host-manager
RUN rm -rf /usr/local/tomcat/webapps/examples
RUN rm -rf /usr/local/tomcat/webapps/docs


#COPY ./target/FinalProject.war /usr/local/tomcat/webapps/ROOT.war
#COPY ./target/FinalProject/. /usr/local/tomcat/webapps/ROOT/.

CMD ["sh", "/entrypoint.sh"]