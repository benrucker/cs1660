FROM sonarqube
ADD https://binaries.sonarsource.com/Distribution/sonar-scanner-cli/sonar-scanner-cli-4.6.2.2472-linux.zip /tmp/sonar-scanner.zip
RUN apk add --no-cache zip unzip
RUN unzip /tmp/sonar-scanner.zip -d /opt
RUN rm /tmp/sonar-scanner.zip
RUN chmod +x /opt/sonar-scanner-4.6.2.2472-linux/bin/sonar-scanner
RUN sed -i 's/use_embedded_jre=true/use_embedded_jre=false/g' /opt/sonar-scanner-4.6.2.2472-linux/bin/sonar-scanner
RUN mkdir -p /opt/sonar-scanner-4.6.2.2472-linux/conf
RUN echo "sonar.host.url=http://localhost:9000" > /opt/sonar-scanner-4.6.2.2472-linux/conf/sonar-scanner.properties
RUN echo "sonar.projectKey=sonarqube" >> /opt/sonar-scanner-4.6.2.2472-linux/conf/sonar-scanner.properties
RUN echo "sonar.projectName=sonarqube" >> /opt/sonar-scanner-4.6.2.2472-linux/conf/sonar-scanner.properties

# todo: run a script to attempt to make a default project on sonarqube
#       and change the default password
