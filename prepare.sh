#!/usr/bin/env bash

set -e

FLINK_VERSION='1.20.0'
FLINK_CDC_VERSION='3.2.1'

# Remove artifact downloading directory
rm -rf ./opt
mkdir -p ./tmp

if [ ! -e "./tmp/flink-${FLINK_VERSION}-bin-scala_2.12.tgz" ]
then
  echo "[INFO] Downloading flink-${FLINK_VERSION}-bin-scala_2.12.tgz"
  wget "https://dlcdn.apache.org/flink/flink-${FLINK_VERSION}/flink-${FLINK_VERSION}-bin-scala_2.12.tgz" -O "./tmp/flink-${FLINK_VERSION}-bin-scala_2.12.tgz"
else
  echo "[INFO] Using cached flink-${FLINK_VERSION}-bin-scala_2.12.tgz"
fi

mkdir -p ./opt/flink
tar -xzf "./tmp/flink-${FLINK_VERSION}-bin-scala_2.12.tgz" -C ./opt/flink --strip-components=1


if [ ! -e "./tmp/flink-cdc-${FLINK_CDC_VERSION}-bin.tar.gz" ]
then
  echo "[INFO] Downloading flink-cdc-${FLINK_CDC_VERSION}-bin.tar.gz"
  wget "https://dlcdn.apache.org/flink/flink-cdc-${FLINK_CDC_VERSION}/flink-cdc-${FLINK_CDC_VERSION}-bin.tar.gz" -O "./tmp/flink-cdc-${FLINK_CDC_VERSION}-bin.tar.gz"
else
  echo "[INFO] Using cached flink-cdc-${FLINK_CDC_VERSION}-bin.tar.gz"
fi

mkdir -p ./opt/flink-cdc
tar -xzf "./tmp/flink-cdc-${FLINK_CDC_VERSION}-bin.tar.gz" -C ./opt/flink-cdc --strip-components=1


function download() {
  for connectorName in "$@"
  do
    tmpPath="./tmp/flink-cdc-pipeline-connector-${connectorName}-${FLINK_CDC_VERSION}.jar"
    targetPath="./opt/flink-cdc/lib/flink-cdc-pipeline-connector-${connectorName}-${FLINK_CDC_VERSION}.jar"
    if [ ! -e targetPath ]
    then
      echo "Downloading ${connectorName} pipeline connector..."
      wget "https://repo1.maven.org/maven2/org/apache/flink/flink-cdc-pipeline-connector-${connectorName}/${FLINK_CDC_VERSION}/flink-cdc-pipeline-connector-${connectorName}-${FLINK_CDC_VERSION}.jar" -O "${tmpPath}"
    else
      echo "[INFO] Using cached flink-cdc-pipeline-connector-${connectorName}-${FLINK_CDC_VERSION}.jar"
    fi
    cp "${tmpPath}" "${targetPath}"
  done
}

download "mysql" "doris" "starrocks" "kafka" "paimon" "elasticsearch" "values"
