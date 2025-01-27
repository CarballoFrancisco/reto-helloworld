pipeline {
    agent none  // No se asigna un agente global al principio

    stages {
        // Etapa de clonación del repositorio y verificación de archivos
        stage('Clonar repositorio y verificar archivos') {
            agent { label 'agente1' }  // Asignar esta etapa al agente1
            steps {
                echo "Ejecutando en agente: ${env.NODE_NAME}"
                bat 'whoami'
                bat 'hostname'
                echo "El espacio de trabajo es: ${env.WORKSPACE}"
                git 'https://github.com/CarballoFrancisco/reto-helloworld.git'
                bat 'dir'
                stash includes: '**/*', name: 'repoFiles'  // Stash de los archivos del repositorio
            }
        }

        // Etapa para verificar espacio de trabajo en un segundo agente
        stage('Verificar espacio de trabajo') {
            agent { label 'agente2' }  // Asignar esta etapa al agente2
            steps {
                echo "Ejecutando en agente: ${env.NODE_NAME}"
                bat 'whoami'
                bat 'hostname'
                echo "El espacio de trabajo es: ${env.WORKSPACE}"
                unstash 'repoFiles'  // Recuperar archivos del stash
            }
        }

        // Etapa de Build
        stage('Build') {
            agent { label 'agente2' }  // Asignar esta etapa al agente2
            steps {
                echo "Ejecutando en agente: ${env.NODE_NAME}"
                bat 'whoami'
                bat 'hostname'
                echo "El espacio de trabajo es: ${env.WORKSPACE}"
                echo 'Realizando la compilación o proceso de build'
            }
        }

        // Etapa de pruebas unitarias
        stage('unit') {
            agent { label 'agente1' }  // Asignar esta etapa al agente1
            steps {
                catchError(buildResult: 'UNSTABLE', stageResult: 'FAILURE') {
                    echo "Ejecutando en agente: ${env.NODE_NAME}"
                    bat 'whoami'
                    bat 'hostname'
                    echo "El espacio de trabajo es: ${env.WORKSPACE}"
                    bat 'set PYTHONPATH=%WORKSPACE%\\'
                    bat 'python -m pytest --junitxml=result-unit.xml test\\unit'
                    stash includes: 'result-unit.xml', name: 'unitTestResults'  // Stash de resultados de las pruebas unitarias
                }
            }
        }

        // Etapa de pruebas REST
        stage('Rest') {
            agent { label 'agente2' }  // Asignar esta etapa al agente2
            steps {
                echo "Ejecutando en agente: ${env.NODE_NAME}"
                bat 'whoami'
                bat 'hostname'
                echo "El espacio de trabajo es: ${env.WORKSPACE}"
                unstash 'unitTestResults'  // Recuperar resultados de pruebas unitarias
                bat '''
                    docker run -d --name wiremock -p 9090:8080 -v C:/ProgramData/Jenkins/.jenkins/workspace/casoPractico1/test/wiremock/mappings:/home/wiremock/mappings wiremock/wiremock:latest
                    set FLASK_APP=C:/ProgramData/Jenkins/.jenkins/workspace/reto1/app/api.py
                    start /B python -m flask run --host=0.0.0.0 --port=5000
                    set PYTHONPATH=%WORKSPACE%
                    pytest --junitxml=result-rest.xml test\\rest
                '''
                stash includes: 'result-rest.xml', name: 'restTestResults'  // Stash de resultados de las pruebas REST
            }
        }
    }
}


