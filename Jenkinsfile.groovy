pipeline {
    agent any

    stages {
        stage('Get Code') {
            steps {
                git 'https://github.com/CarballoFrancisco/reto-helloworld.git'
                bat 'dir'
                echo "WORKSPACE: ${env.WORKSPACE}"
            }
        }

        stage('Unit') {
            steps {
                catchError(buildResult: 'UNSTABLE', stageResult: 'FAILURE') {
                    bat 'set PYTHONPATH=%WORKSPACE%\\'
                    bat 'python -m pytest --junitxml=result-unit.xml test\\unit'
                    junit 'result*.xml'
                    bat 'python -m coverage run --branch --source=app --omit=app\\_init.py,app\\api.py -m pytest test\\unit'
                    bat 'python -m coverage xml'
                }
            }
        }

        stage('Rest') {
            steps {
                script {
                    echo 'Iniciando WireMock en Docker'
                    bat '''
                        docker run -d --name wiremock -p 9090:8080 wiremock/wiremock:latest
                    '''
                }
            }
        }

        stage('Static') {
            steps {
                catchError(buildResult: 'UNSTABLE', stageResult: 'FAILURE') {
                    script {
                        bat 'flake8 --exit-zero --format=pylint app >flake8.out'
                        recordIssues tools: [flake8(name: 'Flake8', pattern: 'flake8.out')],
                                     qualityGates: [
                                         [threshold: 8, type: 'TOTAL', unstable: true],
                                         [threshold: 10, type: 'TOTAL', unstable: false]
                                     ]
                    }
                }
            }
        }

        stage('Security') {
            steps {
                script {
                    bat '''
                        bandit --exit-zero -r . -f custom -o bandit.out --msg-template "{abspath}:{line}: [{test_id}]: {msg}"
                    '''
                }
                recordIssues tools: [pyLint(name: 'Bandit', pattern: 'bandit.out')],
                             qualityGates: [
                                 [threshold: 2, type: 'TOTAL', unstable: true],
                                 [threshold: 4, type: 'TOTAL', unstable: false]
                             ]
            }
        }

        stage('Coverage') {
            steps {
                script {

                    cobertura coberturaReportFile: 'coverage.xml',
                              lineCoverageTargets: '95,0,85',
                              conditionalCoverageTargets: '90,0,80',
                              onlyStable: false
                }
            }
        }

        stage('Performance') {
            steps {
                bat '''
                    set FLASK_APP=C:/ProgramData/Jenkins/.jenkins/workspace/test1/app/api.py
                    start /B flask run
                    "C:\\Users\\carba\\Desktop\\apache-jmeter-5.6.3\\apache-jmeter-5.6.3\\bin\\jmeter" -n -t "test\\jmeter\\flask.jmx" -f -l "flask.jtl"
                '''
                perfReport sourceDataFiles: 'flask.jtl'
            }
        }
    }
}
