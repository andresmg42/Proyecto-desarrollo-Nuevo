# Configura tus variables
$SonarProjectKey = "andresmg42_Proyecto-desarrollo-Nuevo"
$SonarToken = "squ_ff02ee0d54427ae76d7728b9f66ae701bb2c2db7"
$SonarHost = "http://host.docker.internal:9000"

# Ejecutar tests y generar reporte de cobertura
Write-Host "Ejecutando tests con cobertura..."
coverage run manage.py test
coverage xml

# Verificar si el archivo de cobertura se generó
if (!(Test-Path "coverage.xml")) {
    Write-Host "coverage.xml no fue generado. Verifica que coverage esté instalado y configurado."
    exit 1
}

# Ejecutar SonarScanner en Docker
Write-Host " Ejecutando SonarScanner dentro de un contenedor Docker..."
docker run --rm `
  -e SONAR_HOST_URL=$SonarHost `
  -e SONAR_LOGIN=$SonarToken `
  -v "${PWD}:/usr/src" `
  -w /usr/src `
  sonarsource/sonar-scanner-cli