#!/usr/bin/env python3
"""
Kubernetes Bare Metal Installation Tutorial Server
Simple HTTP server to serve the Kubernetes tutorial website
"""

import http.server
import socketserver
import os
import sys
import json
from pathlib import Path
from urllib.parse import urlparse, parse_qs

class KubernetesServerHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        # Set the directory to serve files from
        super().__init__(*args, directory=os.path.dirname(os.path.abspath(__file__)), **kwargs)

    def do_GET(self):
        """Handle GET requests"""
        path = urlparse(self.path).path
        
        if path == '/':
            self.serve_home()
        elif path == '/kubernetes-tutorial':
            self.serve_kubernetes_tutorial()
        elif path == '/api/health':
            self.serve_health_check()
        elif path.startswith('/static/'):
            # Serve static files
            super().do_GET()
        else:
            # Default behavior for other paths
            super().do_GET()

    def serve_home(self):
        """Serve the home page with API info and tutorial link"""
        content = json.dumps({
            "message": "Face Recognition API is running",
            "tutorial": "Visit /kubernetes-tutorial for Kubernetes bare metal installation guide",
            "api_endpoints": [
                "GET / - This information",
                "GET /api/health - Health check",
                "GET /kubernetes-tutorial - Kubernetes tutorial website"
            ]
        }, indent=2)
        
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(content.encode('utf-8'))

    def serve_health_check(self):
        """Serve health check endpoint"""
        content = json.dumps({"status": "healthy"})
        
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(content.encode('utf-8'))

    def serve_kubernetes_tutorial(self):
        """Serve the Kubernetes tutorial HTML page"""
        html_content = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Kubernetes Bare Metal Installation Tutorial</title>
    <link rel="stylesheet" href="/static/css/style.css">
</head>
<body>
    <header>
        <nav>
            <h1>Kubernetes Bare Metal Installation Tutorial</h1>
            <ul>
                <li><a href="#overview">Overview</a></li>
                <li><a href="#prerequisites">Prerequisites</a></li>
                <li><a href="#installation">Installation</a></li>
                <li><a href="#configuration">Configuration</a></li>
                <li><a href="#troubleshooting">Troubleshooting</a></li>
            </ul>
        </nav>
    </header>
    
    <main>
        <section id="overview">
            <h2>Overview</h2>
            <p>This comprehensive guide will walk you through installing Kubernetes on bare metal servers. Kubernetes on bare metal provides better performance, security, and cost-effectiveness compared to cloud solutions for certain use cases.</p>
            
            <h3>What You'll Learn</h3>
            <ul>
                <li>How to prepare your bare metal environment</li>
                <li>Installing and configuring the Kubernetes control plane</li>
                <li>Setting up worker nodes</li>
                <li>Configuring networking with Calico or Flannel</li>
                <li>Common troubleshooting techniques</li>
            </ul>
        </section>

        <section id="prerequisites">
            <h2>Prerequisites</h2>
            
            <h3>Hardware Requirements</h3>
            <div class="requirement-box">
                <h4>Control Plane Node (Master)</h4>
                <ul>
                    <li><strong>CPU:</strong> 2+ cores</li>
                    <li><strong>RAM:</strong> 2GB minimum (4GB recommended)</li>
                    <li><strong>Storage:</strong> 20GB disk space</li>
                    <li><strong>Network:</strong> Full network connectivity between nodes</li>
                </ul>
            </div>
            
            <div class="requirement-box">
                <h4>Worker Nodes</h4>
                <ul>
                    <li><strong>CPU:</strong> 1+ cores</li>
                    <li><strong>RAM:</strong> 1GB minimum (2GB recommended)</li>
                    <li><strong>Storage:</strong> 10GB disk space</li>
                    <li><strong>Network:</strong> Full network connectivity to control plane</li>
                </ul>
            </div>

            <h3>Software Prerequisites</h3>
            <div class="code-block">
                <h4>Operating System</h4>
                <p>Ubuntu 20.04+ / CentOS 7+ / RHEL 7+ / Debian 9+</p>
                
                <h4>Required Ports</h4>
                <pre>Control Plane:
- 6443: Kubernetes API server
- 2379-2380: etcd server client API
- 10250: kubelet API
- 10251: kube-scheduler
- 10252: kube-controller-manager

Worker Nodes:
- 10250: kubelet API
- 30000-32767: NodePort services</pre>
            </div>
        </section>

        <section id="installation">
            <h2>Installation Steps</h2>
            
            <h3>Step 1: Prepare All Nodes</h3>
            <div class="step">
                <h4>1.1 Disable Swap</h4>
                <div class="code-block">
                    <pre># Disable swap temporarily
sudo swapoff -a

# Disable swap permanently
sudo sed -i '/ swap / s/^\\(.*\\)$/#\\1/g' /etc/fstab</pre>
                </div>
            </div>

            <div class="step">
                <h4>1.2 Configure Kernel Parameters</h4>
                <div class="code-block">
                    <pre># Enable bridge networking
cat &lt;&lt;EOF | sudo tee /etc/modules-load.d/k8s.conf
overlay
br_netfilter
EOF

sudo modprobe overlay
sudo modprobe br_netfilter

# Configure sysctl
cat &lt;&lt;EOF | sudo tee /etc/sysctl.d/k8s.conf
net.bridge.bridge-nf-call-iptables  = 1
net.bridge.bridge-nf-call-ip6tables = 1
net.ipv4.ip_forward                 = 1
EOF

sudo sysctl --system</pre>
                </div>
            </div>

            <div class="step">
                <h4>1.3 Install Container Runtime (containerd)</h4>
                <div class="code-block">
                    <pre># Install containerd
sudo apt-get update
sudo apt-get install -y containerd

# Configure containerd
sudo mkdir -p /etc/containerd
containerd config default | sudo tee /etc/containerd/config.toml

# Restart containerd
sudo systemctl restart containerd
sudo systemctl enable containerd</pre>
                </div>
            </div>

            <div class="step">
                <h4>1.4 Install Kubernetes Components</h4>
                <div class="code-block">
                    <pre># Add Kubernetes repository
curl -fsSL https://packages.cloud.google.com/apt/doc/apt-key.gpg | sudo apt-key add -
echo "deb https://apt.kubernetes.io/ kubernetes-xenial main" | sudo tee /etc/apt/sources.list.d/kubernetes.list

# Install kubelet, kubeadm, and kubectl
sudo apt-get update
sudo apt-get install -y kubelet kubeadm kubectl
sudo apt-mark hold kubelet kubeadm kubectl

# Enable kubelet
sudo systemctl enable kubelet</pre>
                </div>
            </div>

            <h3>Step 2: Initialize Control Plane</h3>
            <div class="step">
                <h4>2.1 Initialize the Cluster</h4>
                <div class="code-block">
                    <pre># Initialize the control plane (replace with your pod network CIDR)
sudo kubeadm init --pod-network-cidr=10.244.0.0/16

# Set up kubectl for regular user
mkdir -p $HOME/.kube
sudo cp -i /etc/kubernetes/admin.conf $HOME/.kube/config
sudo chown $(id -u):$(id -g) $HOME/.kube/config</pre>
                </div>
                <div class="important">
                    <strong>Important:</strong> Save the kubeadm join command output! You'll need it to join worker nodes.
                </div>
            </div>

            <h3>Step 3: Install Network Plugin</h3>
            <div class="step">
                <h4>3.1 Install Flannel (Option 1)</h4>
                <div class="code-block">
                    <pre>kubectl apply -f https://raw.githubusercontent.com/flannel-io/flannel/master/Documentation/kube-flannel.yml</pre>
                </div>
            </div>
            
            <div class="step">
                <h4>3.2 Install Calico (Option 2)</h4>
                <div class="code-block">
                    <pre>kubectl create -f https://raw.githubusercontent.com/projectcalico/calico/v3.25.0/manifests/tigera-operator.yaml
kubectl create -f https://raw.githubusercontent.com/projectcalico/calico/v3.25.0/manifests/custom-resources.yaml</pre>
                </div>
            </div>

            <h3>Step 4: Join Worker Nodes</h3>
            <div class="step">
                <h4>4.1 Join Worker Nodes to Cluster</h4>
                <p>On each worker node, run the kubeadm join command from Step 2.1:</p>
                <div class="code-block">
                    <pre>sudo kubeadm join &lt;control-plane-ip&gt;:6443 --token &lt;token&gt; \\
    --discovery-token-ca-cert-hash sha256:&lt;hash&gt;</pre>
                </div>
            </div>
        </section>

        <section id="configuration">
            <h2>Post-Installation Configuration</h2>
            
            <h3>Verify Cluster Status</h3>
            <div class="code-block">
                <pre># Check node status
kubectl get nodes

# Check system pods
kubectl get pods -n kube-system

# Check cluster info
kubectl cluster-info</pre>
            </div>

            <h3>Install Dashboard (Optional)</h3>
            <div class="code-block">
                <pre># Install Kubernetes Dashboard
kubectl apply -f https://raw.githubusercontent.com/kubernetes/dashboard/v2.7.0/aio/deploy/recommended.yaml

# Create admin user
kubectl create serviceaccount dashboard-admin-sa
kubectl create clusterrolebinding dashboard-admin-sa --clusterrole=cluster-admin --serviceaccount=default:dashboard-admin-sa

# Get access token
kubectl secrets list
kubectl describe secret &lt;dashboard-admin-sa-token&gt;</pre>
            </div>
        </section>

        <section id="troubleshooting">
            <h2>Troubleshooting</h2>
            
            <h3>Common Issues</h3>
            
            <div class="troubleshoot-item">
                <h4>Issue: Nodes not joining the cluster</h4>
                <p><strong>Solution:</strong></p>
                <ul>
                    <li>Check firewall rules and ensure required ports are open</li>
                    <li>Verify network connectivity between nodes</li>
                    <li>Ensure containerd is running on all nodes</li>
                    <li>Check token expiration (tokens expire after 24 hours)</li>
                </ul>
                <div class="code-block">
                    <pre># Generate new token if expired
kubeadm token create --print-join-command</pre>
                </div>
            </div>

            <div class="troubleshoot-item">
                <h4>Issue: Pods stuck in Pending state</h4>
                <p><strong>Solution:</strong></p>
                <ul>
                    <li>Check if network plugin is installed and working</li>
                    <li>Verify sufficient resources on nodes</li>
                    <li>Check for taints on nodes</li>
                </ul>
                <div class="code-block">
                    <pre># Describe pod to see why it's pending
kubectl describe pod &lt;pod-name&gt;

# Check node capacity
kubectl top nodes

# Remove taints if necessary
kubectl taint nodes --all node-role.kubernetes.io/control-plane-</pre>
                </div>
            </div>

            <div class="troubleshoot-item">
                <h4>Issue: DNS not working</h4>
                <p><strong>Solution:</strong></p>
                <div class="code-block">
                    <pre># Check CoreDNS pods
kubectl get pods -n kube-system | grep coredns

# Restart CoreDNS if needed
kubectl rollout restart deployment/coredns -n kube-system

# Test DNS resolution
kubectl run test-dns --image=busybox -it --rm --restart=Never -- nslookup kubernetes.default</pre>
                </div>
            </div>

            <h3>Useful Commands</h3>
            <div class="code-block">
                <pre># View logs
kubectl logs -n kube-system &lt;pod-name&gt;

# Get events
kubectl get events --sort-by=.metadata.creationTimestamp

# Describe resources
kubectl describe node &lt;node-name&gt;
kubectl describe pod &lt;pod-name&gt;

# Check kubelet logs
sudo journalctl -u kubelet -f</pre>
            </div>
        </section>

        <section class="conclusion">
            <h2>Conclusion</h2>
            <p>You now have a fully functional Kubernetes cluster running on bare metal! This setup provides you with:</p>
            <ul>
                <li>Complete control over your infrastructure</li>
                <li>Better performance compared to virtualized environments</li>
                <li>Cost savings over managed cloud solutions</li>
                <li>Learning opportunity with hands-on Kubernetes administration</li>
            </ul>
            
            <h3>Next Steps</h3>
            <ul>
                <li>Deploy sample applications</li>
                <li>Set up monitoring with Prometheus and Grafana</li>
                <li>Configure ingress controllers</li>
                <li>Implement backup and disaster recovery</li>
                <li>Set up CI/CD pipelines</li>
            </ul>
        </section>
    </main>

    <footer>
        <p>&copy; 2024 Kubernetes Bare Metal Installation Tutorial. For more resources, visit the <a href="/">API Documentation</a>.</p>
    </footer>

    <script src="/static/js/tutorial.js"></script>
</body>
</html>"""

        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(html_content.encode('utf-8'))

    def log_message(self, format, *args):
        """Override to provide better logging"""
        print(f"[{self.date_time_string()}] {format % args}")

def run_server(port=8000):
    """Run the HTTP server"""
    handler = KubernetesServerHandler
    
    with socketserver.TCPServer(("", port), handler) as httpd:
        print(f"🚀 Kubernetes Tutorial Server running at http://localhost:{port}")
        print(f"📚 Visit http://localhost:{port}/kubernetes-tutorial for the tutorial")
        print(f"💻 API available at http://localhost:{port}/")
        print(f"Press Ctrl+C to stop the server")
        
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n🛑 Server stopped.")

if __name__ == "__main__":
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8000
    run_server(port)