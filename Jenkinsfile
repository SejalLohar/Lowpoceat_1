pipeline {
  agent any

  environment {
    // adjust if your Nexus uses a different host/port
    NEXUS_REGISTRY = "localhost:5001"
    IMAGE_NAME = "${NEXUS_REGISTRY}/django-app"
    // Jenkins credentials IDs (create these in Jenkins credentials store)
    NEXUS_CRED_ID = "nexus-creds"
    GIT_CRED_ID = "github-creds"           // optional (if private repo)
    SONAR_TOKEN_CRED = "sonar-token"       // as "Secret text"
    // Optional AWS creds (if you use AWS deploy stage)
    AWS_CRED_ID = "aws-creds"
  }

  options {
    // keep build logs for some time
    timestamps()
    ansiColor('xterm')
  }

  stages {
    stage('Checkout') {
      steps {
        script {
          // if private, Jenkins will use credential configured on job/multibranch
          checkout scm
        }
      }
    }

    stage('Setup Python (optional)') {
      steps {
        // This stage is optional but useful if you want to run tests or linters in Jenkins.
        // We use a lightweight approach: install requirements in workspace's venv
        sh '''
          python3 -m venv .venv || true
          . .venv/bin/activate
          pip install --upgrade pip
          if [ -f requirements.txt ]; then pip install -r requirements.txt; fi
        '''
      }
    }

    stage('Run Tests') {
      steps {
        // run your Django tests (optional). Adjust manage.py path if needed.
        sh '''
          . .venv/bin/activate || true
          if [ -f manage.py ]; then
            python manage.py test || true
          fi
        '''
      }
    }

    stage('SonarQube Analysis') {
      environment {
        SONAR_TOKEN = credentials(SONAR_TOKEN_CRED)
      }
      steps {
        script {
          // Using sonar-scanner CLI. Ensure SonarQube Scanner is available on Jenkins nodes
          // or install it via Jenkins Global Tool Configuration.
          sh '''
            # create sonar-project.properties dynamically
            cat > sonar-project.properties <<EOF
            sonar.projectKey=Lowpoceat_1
            sonar.projectName=Lowpoceat_1
            sonar.projectVersion=1.0
            sonar.sources=.
            sonar.python.version=3
            sonar.sourceEncoding=UTF-8
            EOF

            # run scanner (requires sonar-scanner on PATH or configured in Jenkins)
            sonar-scanner -Dsonar.login=${SONAR_TOKEN}
          '''
        }
      }
    }

    stage('Build Docker Image') {
      steps {
        script {
          sh "docker build -t ${IMAGE_NAME}:latest ."
        }
      }
    }

    stage('Push to Nexus') {
      steps {
        script {
          // Use Docker CLI + credentials stored in Jenkins
          withCredentials([usernamePassword(credentialsId: NEXUS_CRED_ID, usernameVariable: 'NEX_USR', passwordVariable: 'NEX_PSW')]) {
            sh '''
              echo "${NEX_PSW}" | docker login http://${NEXUS_REGISTRY} -u "${NEX_USR}" --password-stdin
              docker tag ${IMAGE_NAME}:latest ${IMAGE_NAME}:$BUILD_NUMBER || true
              docker push ${IMAGE_NAME}:latest
              docker push ${IMAGE_NAME}:$BUILD_NUMBER || true
              docker logout ${NEXUS_REGISTRY}
            '''
          }
        }
      }
    }

    stage('Deploy to AWS (optional)') {
      when {
        expression { return params.DEPLOY_TO_AWS == true }
      }
      environment {
        AWS_CREDS = credentials(AWS_CRED_ID)
      }
      steps {
        script {
          // Example: push image to EC2 and run docker-compose or ssh deploy.
          // You must have AWS CLI installed or use SSH-based deploy. Placeholder below:
          sh '''
            echo "Deploy stage - implement according to your AWS strategy (ECR/EC2/ECS)."
            # Example (if using SSH to EC2):
            # scp docker-compose.yml ubuntu@EC2_IP:/home/ubuntu/
            # ssh ubuntu@EC2_IP "docker pull ${IMAGE_NAME}:latest && docker-compose up -d"
          '''
        }
      }
    }
  }

  post {
    success {
      echo "Pipeline finished successfully."
    }
    failure {
      echo "Pipeline failed. Check console output."
    }
    always {
      cleanWs()
    }
  }
}
