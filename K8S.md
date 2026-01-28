# Setting up a Kubernetes Cluster on Proxmox with K3s

This guide outlines the fastest and most common method for creating a robust Kubernetes cluster in a Proxmox homelab environment using K3s.

### Why K3s on Proxmox?

**K3s** is a lightweight, fully compliant Kubernetes distribution that is ideal for homelabs. It's fast to install, has a small resource footprint, and is very easy to manage. Running it on Virtual Machines (VMs) in Proxmox gives you a stable and scalable setup.

---

## Quick Steps to Create a K3s Cluster

This process typically takes less than 30 minutes.

### 1. Create a VM Template (Optional but Recommended)

To speed up future deployments, it's best to create a reusable template.

1.  Create a new VM in Proxmox using a lightweight Linux distribution like **Ubuntu Server** or **Debian**.
2.  During setup, ensure you install the **OpenSSH server**.
3.  Once the OS is installed, log into the VM and run system updates:
    ```bash
    sudo apt update && sudo apt upgrade -y
    ```
4.  Install the QEMU Guest Agent for better integration with Proxmox:
    ```bash
    sudo apt install qemu-guest-agent
    ```
5.  Shut down the VM.
6.  In the Proxmox UI, right-click the VM and select **"Convert to template"**.

### 2. Create Your Cluster VMs

1.  Right-click your new template and **"Clone"** it.
2.  Create at least two VMs:
    *   One "server" node (e.g., `k3s-server`).
    *   One or more "agent" nodes (e.g., `k3s-agent-1`).
3.  In the "Hardware" tab for each VM, give them at least **2 CPU cores** and **2GB of RAM**.
4.  Start all the VMs.

### 3. Install the K3s Server (Control Plane)

1.  Find the IP address of your server VM (`k3s-server`).
2.  SSH into the server VM:
    ```bash
    ssh your_user@<k3s-server-ip>
    ```
3.  Run the following command to install K3s. The `write-kubeconfig-mode 644` flag makes the config file readable by your user, which is convenient for using `kubectl` without `sudo`.
    ```bash
    curl -sfL https://get.k3s.io | sh -s - --write-kubeconfig-mode 644
    ```
4.  After a minute, verify the installation on the server:
    ```bash
    kubectl get nodes
    ```
    You should see your `k3s-server` node listed with a "Ready" status.

### 4. Get the Join Token and Server IP

You'll need two pieces of information from the `k3s-server` to join the other nodes.

1.  **Get the Server IP:**
    You should already have this, but you can run `ip a` to confirm.

2.  **Get the Join Token:**
    On the `k3s-server`, run this command to display the secret token:
    ```bash
    sudo cat /var/lib/rancher/k3s/server/node-token
    ```
    Copy this token value.

### 5. Install K3s on the Agent(s)

1.  SSH into each of your agent VMs (`k3s-agent-1`, etc.).
2.  Run the following command, replacing `<SERVER_IP>` and `<YOUR_TOKEN>` with the values from the previous step:
    ```bash
    curl -sfL https://get.k3s.io | K3S_URL=https://<SERVER_IP>:6443 K3S_TOKEN=<YOUR_TOKEN> sh -
    ```
3.  This script will install the K3s agent and connect it to the server.

### 6. Verify Your Cluster

1.  Go back to your SSH session on the **`k3s-server`** VM.
2.  Run `kubectl get nodes` again.
    ```bash
    kubectl get nodes
    ```
3.  You should now see all your agent nodes listed with a "Ready" status. This may take a minute or two to update.

**Congratulations, you now have a fully functional Kubernetes cluster running on your Proxmox server!**

---

### Other Good Options (More Complex)

While K3s is the fastest, these are other powerful methods for a Proxmox environment:

*   **Kubeadm:** The "official" but more manual way to bootstrap a cluster. It's a great learning experience for understanding the components of Kubernetes.
*   **Talos OS:** A modern, secure, and immutable operating system built specifically for Kubernetes. It uses a declarative YAML file for configuration, making it very robust for a permanent homelab.
