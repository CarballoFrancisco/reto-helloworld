pipeline {
    agent any

    stages {
        stage('Clonar repositorio y verificar archivos') {
            steps {
                git 'https://github.com/CarballoFrancisco/reto-helloworld.git'
                bat 'dir'
            }
        }

        stage('Verificar espacio de trabajo') {
            steps {
                script {
                    echo "El espacio de trabajo es: ${env.WORKSPACE}"
                }
            }
        }

        stage('Build') {
            steps {
                // Simulación de sobrecarga
                bat '''
                    python -c "import math; [math.sqrt(i) for i in range(10000000)]"
                '''
            }
        }

        stage('Pruebas en paralelo') {
            parallel {
                stage('Unit') {
                    steps {
                        catchError(buildResult: 'UNSTABLE', stageResult: 'FAILURE') {
                            bat 'set PYTHONPATH=%WORKSPACE%\\'
                            bat 'python -m pytest --junitxml=result-unit.xml test\\unit'
                        }
                    }
                }
                stage('Rest') {
                    steps {
                        script {
                            // Iniciar Wiremock y Flask
                            bat '''
                                docker run -d --name wiremock -p 9090:8080 -v C:/ProgramData/Jenkins/.jenkins/workspace/casoPractico1/test/wiremock/mappings:/home/wiremock/mappings wiremock/wiremock:latest
                                set FLASK_APP=C:/ProgramData/Jenkins/.jenkins/workspace/reto1/app/api.py
                                start /B python -m flask run --host=0.0.0.0 --port=5000
                            '''
                            
                            // Esperar a que los servicios estén listos (alternativa a timeout)
                            echo "Esperando que los servicios estén listos..."
                            bat '''
                                ping -n 31 127.0.0.1 > nul
                            '''
                            
                            // Ejecutar pruebas REST
                            bat '''
                                set PYTHONPATH=%WORKSPACE%
                                pytest --junitxml=result-rest.xml test\\rest
                            '''
                        }
                    }
                }
            }
        }
        
        stage('Results') {
            steps {
                // Publicar los resultados de las pruebas
                junit 'result-unit.xml'
                junit 'result-rest.xml'
            }
        }
    }
}



