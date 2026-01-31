"""
Interview Trends Based Fine-tuning Data Generator
Generates training data based on current 2026 interview trends and best practices
"""

import json
import boto3
from datetime import datetime
from typing import List, Dict

class InterviewTrendsDataGenerator:
    """Generate fine-tuning data based on current interview trends"""
    
    def __init__(self):
        self.s3_client = boto3.client('s3', region_name='us-east-1')
        self.bucket_name = 'interview-coach-training-data-dev'
        self.trends_2026 = {
            'system_design': True,
            'behavioral': True,
            'problem_solving': True,
            'ai_ml_awareness': True,
            'remote_collaboration': True,
            'security_awareness': True,
            'cost_optimization': True
        }
    
    def generate_python_backend_trends(self) -> List[Dict]:
        """Python Backend trends: FastAPI, async, microservices, AI integration"""
        return [
            {
                "role": "Python Backend Engineer",
                "level": "junior",
                "trend": "FastAPI & Modern Python",
                "question": "Explain the difference between sync and async functions in Python. When would you use FastAPI over Flask?",
                "expected_answer": "Async functions are non-blocking and improve performance. FastAPI is better for high-concurrency APIs with built-in async support, validation, and OpenAPI docs.",
                "category": "backend",
                "year": 2026
            },
            {
                "role": "Python Backend Engineer",
                "level": "junior",
                "trend": "Database Design",
                "question": "Design a database schema for an e-commerce platform with products, categories, and inventory.",
                "expected_answer": "Use normalized schema: products table (id, name, price), categories (id, name), inventory (product_id, quantity). Add indexes on frequently queried columns.",
                "category": "backend",
                "year": 2026
            },
            {
                "role": "Python Backend Engineer",
                "level": "mid",
                "trend": "Microservices & API Design",
                "question": "How would you design a microservices architecture for a large-scale application? What are the challenges?",
                "expected_answer": "Separate concerns by domain, use API Gateway, implement service discovery, handle distributed transactions with saga pattern. Challenges: network latency, debugging, data consistency.",
                "category": "backend",
                "year": 2026
            },
            {
                "role": "Python Backend Engineer",
                "level": "mid",
                "trend": "Security & Best Practices",
                "question": "What are common security vulnerabilities in REST APIs and how do you prevent them?",
                "expected_answer": "SQL injection (use parameterized queries), CSRF (tokens), auth/authz (JWT/OAuth2), rate limiting, input validation, HTTPS, secure headers.",
                "category": "backend",
                "year": 2026
            },
            {
                "role": "Python Backend Engineer",
                "level": "senior",
                "trend": "System Design & Scalability",
                "question": "Design a real-time notification system that handles millions of notifications per day with guaranteed delivery.",
                "expected_answer": "Use message queue (Redis/RabbitMQ), database for persistence, WebSocket for real-time delivery, implement retry logic, circuit breaker pattern, and horizontal scaling.",
                "category": "backend",
                "year": 2026
            },
            {
                "role": "Python Backend Engineer",
                "level": "senior",
                "trend": "AI/ML Integration",
                "question": "How would you integrate an ML model into a production Python backend? What are the challenges?",
                "expected_answer": "Use model serving (TensorFlow Serving, FastAPI), implement versioning, A/B testing, monitoring, and fallback mechanisms. Handle latency, scaling, and model updates.",
                "category": "backend",
                "year": 2026
            },
            {
                "role": "Python Backend Engineer",
                "level": "senior",
                "trend": "Performance Optimization",
                "question": "Your API is slow (5s response time). How do you identify and fix the problem?",
                "expected_answer": "Profile code (cProfile), check database queries (slow logs), implement caching (Redis), optimize algorithms, use async where possible, add CDN for static content.",
                "category": "backend",
                "year": 2026
            },
            {
                "role": "Python Backend Engineer",
                "level": "mid",
                "trend": "Testing & CI/CD",
                "question": "What testing strategy would you implement for a critical payment service?",
                "expected_answer": "Unit tests (pytest), integration tests, contract testing with payment API, end-to-end tests, load testing, chaos engineering, and automated deployment pipeline.",
                "category": "backend",
                "year": 2026
            }
        ]
    
    def generate_react_frontend_trends(self) -> List[Dict]:
        """React Frontend trends: Performance, state management, accessibility"""
        return [
            {
                "role": "React Frontend Engineer",
                "level": "junior",
                "trend": "React Hooks & State Management",
                "question": "Explain useState and useEffect hooks. When would you use useCallback or useMemo?",
                "expected_answer": "useState manages component state, useEffect handles side effects. useCallback memoizes functions, useMemo memoizes values - use when props change frequently or computations are expensive.",
                "category": "frontend",
                "year": 2026
            },
            {
                "role": "React Frontend Engineer",
                "level": "junior",
                "trend": "Component Design",
                "question": "What's the difference between controlled and uncontrolled components?",
                "expected_answer": "Controlled components: state managed by React (form value in state). Uncontrolled: DOM manages state (access via ref). Use controlled for validation, uncontrolled for simple forms.",
                "category": "frontend",
                "year": 2026
            },
            {
                "role": "React Frontend Engineer",
                "level": "mid",
                "trend": "Performance Optimization",
                "question": "Your React app is slow. Identify performance issues and optimize it.",
                "expected_answer": "Use React DevTools Profiler, implement code splitting (lazy loading), memoize components (React.memo, useMemo), optimize re-renders, use proper keys in lists, and implement virtualization for large lists.",
                "category": "frontend",
                "year": 2026
            },
            {
                "role": "React Frontend Engineer",
                "level": "mid",
                "trend": "State Management at Scale",
                "question": "When would you use Redux vs Context API? What are pros/cons?",
                "expected_answer": "Redux for large apps with complex state, middleware, dev tools. Context for simple state sharing. Redux is more verbose but powerful; Context is lighter but less scalable.",
                "category": "frontend",
                "year": 2026
            },
            {
                "role": "React Frontend Engineer",
                "level": "senior",
                "trend": "Accessibility & UX",
                "question": "How do you ensure your React app is accessible (WCAG 2.1)?",
                "expected_answer": "Use semantic HTML, aria labels, keyboard navigation, focus management, color contrast, test with screen readers, implement skip links, form labels, and alt text.",
                "category": "frontend",
                "year": 2026
            },
            {
                "role": "React Frontend Engineer",
                "level": "senior",
                "trend": "System Design for UX",
                "question": "Design a complex dashboard with real-time data updates, filtering, and export functionality.",
                "expected_answer": "Use WebSocket for real-time, separate data from UI, implement virtualization for large datasets, memoize selectors, debounce filters, implement pagination/infinite scroll.",
                "category": "frontend",
                "year": 2026
            },
            {
                "role": "React Frontend Engineer",
                "level": "senior",
                "trend": "Testing",
                "question": "What testing approach would you use for a critical payment flow?",
                "expected_answer": "Unit tests (vitest/jest), integration tests (React Testing Library), E2E tests (Cypress/Playwright), visual regression testing, accessibility testing, and load testing.",
                "category": "frontend",
                "year": 2026
            }
        ]
    
    def generate_devops_trends(self) -> List[Dict]:
        """DevOps trends: Kubernetes, GitOps, Security, Cost Optimization"""
        return [
            {
                "role": "DevOps Engineer",
                "level": "junior",
                "trend": "Container Basics",
                "question": "Explain Docker containers, images, and registries. What's the benefit of containerization?",
                "expected_answer": "Images are blueprints, containers are running instances. Registries store images. Benefits: consistency, isolation, reproducibility, portability across environments.",
                "category": "devops",
                "year": 2026
            },
            {
                "role": "DevOps Engineer",
                "level": "mid",
                "trend": "Kubernetes Orchestration",
                "question": "Design a Kubernetes deployment for a microservices application with multiple replicas and auto-scaling.",
                "expected_answer": "Create Deployments with replicas, configure HPA based on CPU/memory, use Services for discovery, implement liveness/readiness probes, manage ConfigMaps and Secrets.",
                "category": "devops",
                "year": 2026
            },
            {
                "role": "DevOps Engineer",
                "level": "mid",
                "trend": "GitOps & IaC",
                "question": "What's GitOps? How would you implement it with ArgoCD or Flux?",
                "expected_answer": "Git as single source of truth, automated deployments on Git changes. Tools like ArgoCD sync desired state from Git. Enables reproducibility, auditability, and easy rollbacks.",
                "category": "devops",
                "year": 2026
            },
            {
                "role": "DevOps Engineer",
                "level": "senior",
                "trend": "Security & Compliance",
                "question": "How do you secure a Kubernetes cluster? What are best practices?",
                "expected_answer": "RBAC for access control, Network Policies, Pod Security Standards, image scanning, secrets management (vault), audit logging, network segmentation, regular updates.",
                "category": "devops",
                "year": 2026
            },
            {
                "role": "DevOps Engineer",
                "level": "senior",
                "trend": "Cost Optimization",
                "question": "Reduce cloud costs in a Kubernetes cluster running 100+ pods. Identify areas.",
                "expected_answer": "Right-sizing nodes, spot instances, resource requests/limits, auto-scaling, consolidate workloads, use reserved instances, optimize storage, implement chargeback.",
                "category": "devops",
                "year": 2026
            },
            {
                "role": "DevOps Engineer",
                "level": "senior",
                "trend": "Disaster Recovery",
                "question": "Design a disaster recovery plan for a critical production Kubernetes cluster.",
                "expected_answer": "Regular backups (Velero), multi-region setup, test recovery procedures, document RTO/RPO, implement monitoring/alerting, use GitOps for state recovery.",
                "category": "devops",
                "year": 2026
            }
        ]
    
    def generate_data_scientist_trends(self) -> List[Dict]:
        """Data Science trends: ML/DL, Ethics, LLMs, Model Optimization"""
        return [
            {
                "role": "Data Scientist",
                "level": "junior",
                "trend": "Statistics & Probability",
                "question": "Explain bias-variance tradeoff. How do you detect overfitting vs underfitting?",
                "expected_answer": "Bias: model's error from wrong assumptions (underfitting). Variance: sensitivity to training data (overfitting). Detect via train/test curves, cross-validation.",
                "category": "data",
                "year": 2026
            },
            {
                "role": "Data Scientist",
                "level": "mid",
                "trend": "Feature Engineering & Selection",
                "question": "You have 1000 features but only 100 samples. How do you approach this?",
                "expected_answer": "Use dimensionality reduction (PCA, t-SNE), feature selection (correlation, importance), regularization (L1/L2), domain knowledge. Avoid curse of dimensionality.",
                "category": "data",
                "year": 2026
            },
            {
                "role": "Data Scientist",
                "level": "mid",
                "trend": "Model Evaluation",
                "question": "Your dataset is imbalanced (1% positive, 99% negative). What metrics and techniques would you use?",
                "expected_answer": "Use Precision, Recall, F1, AUC-ROC (not accuracy). Techniques: SMOTE oversampling, class weights, stratified k-fold, threshold tuning.",
                "category": "data",
                "year": 2026
            },
            {
                "role": "Data Scientist",
                "level": "senior",
                "trend": "Deep Learning & Neural Networks",
                "question": "Design a CNN architecture for image classification with 1000 classes.",
                "expected_answer": "Use ResNet/EfficientNet pretrained, fine-tune last layers, data augmentation, batch norm, dropout, adaptive learning rate, regularization, ensemble models.",
                "category": "data",
                "year": 2026
            },
            {
                "role": "Data Scientist",
                "level": "senior",
                "trend": "Large Language Models & Prompting",
                "question": "How do you fine-tune an LLM for a specific task? What are challenges?",
                "expected_answer": "Prepare domain data, use QLoRA/LoRA for efficiency, prompt engineering, evaluate on test set. Challenges: data quality, compute, catastrophic forgetting, alignment.",
                "category": "data",
                "year": 2026
            },
            {
                "role": "Data Scientist",
                "level": "senior",
                "trend": "Responsible AI & Ethics",
                "question": "How do you detect and mitigate bias in ML models?",
                "expected_answer": "Analyze training data distribution, test across demographic groups, use fairness metrics (disparate impact), implement mitigation techniques, document limitations.",
                "category": "data",
                "year": 2026
            }
        ]
    
    def generate_qa_automation_trends(self) -> List[Dict]:
        """QA Automation trends: Testing frameworks, AI-powered testing, continuous testing"""
        return [
            {
                "role": "QA Automation Engineer",
                "level": "junior",
                "trend": "Test Automation Fundamentals",
                "question": "What's the test pyramid? How do you decide what tests to automate?",
                "expected_answer": "Pyramid: many unit tests, fewer integration tests, few E2E tests. Automate: frequently run tests, critical paths, repetitive tests. Manual: exploratory, UX, edge cases.",
                "category": "qa",
                "year": 2026
            },
            {
                "role": "QA Automation Engineer",
                "level": "mid",
                "trend": "Selenium & Modern Testing",
                "question": "Design a robust test suite for a complex web application with dynamic elements.",
                "expected_answer": "Use WebDriverWait for waits (not sleep), Page Object Model, reliable locators, parallel execution, screenshot on failure, cross-browser testing.",
                "category": "qa",
                "year": 2026
            },
            {
                "role": "QA Automation Engineer",
                "level": "senior",
                "trend": "API & Performance Testing",
                "question": "Design a comprehensive API test strategy for a payment service.",
                "expected_answer": "Contract tests, functional tests (positive/negative), security tests (injection), performance tests, load tests, chaos testing, monitor production API.",
                "category": "qa",
                "year": 2026
            },
            {
                "role": "QA Automation Engineer",
                "level": "senior",
                "trend": "CI/CD & Continuous Testing",
                "question": "Implement a continuous testing pipeline in CI/CD. How do you keep tests fast and reliable?",
                "expected_answer": "Parallel test execution, selective test execution by change, flaky test detection, mock external services, maintain test data, optimize selectors, use proper assertions.",
                "category": "qa",
                "year": 2026
            },
            {
                "role": "QA Automation Engineer",
                "level": "senior",
                "trend": "AI-Powered Testing",
                "question": "How can AI help in test automation? What are use cases and challenges?",
                "expected_answer": "AI for visual testing, test generation, anomaly detection, smart wait strategies. Challenges: training data, model accuracy, interpretability, false positives.",
                "category": "qa",
                "year": 2026
            }
        ]
    
    def generate_fullstack_trends(self) -> List[Dict]:
        """Full Stack trends: MERN, system design, full application development"""
        return [
            {
                "role": "Full Stack Engineer",
                "level": "mid",
                "trend": "MERN Stack Integration",
                "question": "Design a complete MERN application architecture. How do you structure frontend, backend, and database?",
                "expected_answer": "Frontend: React components with state management. Backend: Express.js APIs. Database: MongoDB schemas. Use Docker, implement CI/CD, separate concerns, implement authentication.",
                "category": "fullstack",
                "year": 2026
            },
            {
                "role": "Full Stack Engineer",
                "level": "senior",
                "trend": "End-to-End System Design",
                "question": "Design a Uber-like ride-sharing application. Consider all components and challenges.",
                "expected_answer": "User auth, location services, matching algorithm, real-time updates, payment processing, analytics. Use geospatial databases, WebSockets, microservices, cloud infrastructure.",
                "category": "fullstack",
                "year": 2026
            },
            {
                "role": "Full Stack Engineer",
                "level": "senior",
                "trend": "Scalability & DevOps",
                "question": "How would you scale a monolithic MERN application to handle 1M users?",
                "expected_answer": "Separate frontend/backend, implement caching (Redis), database optimization (sharding), CDN, load balancing, microservices, Kubernetes, monitoring, async processing.",
                "category": "fullstack",
                "year": 2026
            }
        ]
    
    def generate_all_trends_data(self) -> Dict[str, List[Dict]]:
        """Generate all trend-based training data"""
        all_data = {
            'python_backend': self.generate_python_backend_trends(),
            'react_frontend': self.generate_react_frontend_trends(),
            'devops': self.generate_devops_trends(),
            'data_scientist': self.generate_data_scientist_trends(),
            'qa_automation': self.generate_qa_automation_trends(),
            'fullstack': self.generate_fullstack_trends()
        }
        return all_data
    
    def create_jsonl_training_file(self, data: List[Dict], filename: str) -> str:
        """Convert training data to JSONL format"""
        jsonl_content = ''
        for item in data:
            jsonl_content += json.dumps(item) + '\n'
        
        return jsonl_content
    
    def upload_to_s3(self, content: str, filename: str) -> str:
        """Upload training data to S3"""
        try:
            key = f"training-data/{filename}"
            self.s3_client.put_object(
                Bucket=self.bucket_name,
                Key=key,
                Body=content.encode('utf-8'),
                ContentType='application/jsonl'
            )
            return f"s3://{self.bucket_name}/{key}"
        except Exception as e:
            print(f"Error uploading to S3: {e}")
            return None
    
    def generate_and_upload_all(self) -> Dict[str, str]:
        """Generate all training data and upload to S3"""
        all_data = self.generate_all_trends_data()
        results = {}
        
        for category, data in all_data.items():
            filename = f"{category}_trends_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jsonl"
            jsonl_content = self.create_jsonl_training_file(data, filename)
            s3_path = self.upload_to_s3(jsonl_content, filename)
            results[category] = {
                'local_file': filename,
                's3_path': s3_path,
                'samples': len(data),
                'timestamp': datetime.now().isoformat()
            }
            print(f"✓ {category}: {len(data)} samples uploaded to {s3_path}")
        
        return results
    
    def get_trends_summary(self) -> Dict:
        """Get summary of interview trends for 2026"""
        return {
            'year': 2026,
            'key_trends': {
                'system_design': 'Critical for all levels',
                'behavioral': 'Now at par with technical skills',
                'problem_solving': 'Real-world scenario focus',
                'ai_ml_awareness': 'Expected for all roles',
                'remote_collaboration': 'Essential soft skill',
                'security_awareness': 'Non-negotiable',
                'cost_optimization': 'Cloud cost awareness'
            },
            'categories_covered': [
                'Backend Development',
                'Frontend Development',
                'DevOps & Infrastructure',
                'Data Science & ML',
                'QA Automation',
                'Full Stack Development'
            ],
            'difficulty_levels': ['junior', 'mid', 'senior'],
            'total_training_samples': self._calculate_total_samples()
        }
    
    def _calculate_total_samples(self) -> int:
        """Calculate total training samples"""
        all_data = self.generate_all_trends_data()
        return sum(len(data) for data in all_data.values())


if __name__ == '__main__':
    generator = InterviewTrendsDataGenerator()
    
    # Generate all trends data
    print("🚀 Generating Interview Trends Data (2026)...\n")
    all_data = generator.generate_all_trends_data()
    
    # Display summary
    summary = generator.get_trends_summary()
    print(f"📊 Interview Trends Summary:")
    print(f"   Year: {summary['year']}")
    print(f"   Total Training Samples: {summary['total_training_samples']}")
    print(f"   Categories: {len(summary['categories_covered'])}")
    print(f"   Difficulty Levels: {len(summary['difficulty_levels'])}\n")
    
    print(f"🔑 Key Trends:")
    for trend, description in summary['key_trends'].items():
        print(f"   • {trend.title()}: {description}")
    
    print(f"\n📚 Data by Category:")
    for category, data in all_data.items():
        print(f"   • {category}: {len(data)} samples")
    
    # Save to local files
    for category, data in all_data.items():
        filename = f"data/{category}_trends.jsonl"
        with open(filename, 'w') as f:
            for item in data:
                f.write(json.dumps(item) + '\n')
        print(f"✓ Saved {filename}")
