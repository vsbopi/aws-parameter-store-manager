"""
GUI Application for AWS Parameter Store Manager
"""

import threading
import tkinter as tk
from datetime import datetime
from tkinter import filedialog, messagebox, scrolledtext, ttk

from aws_parameter_manager import AWSParameterManager
from config import AuthMethod, aws_config


class ParameterStoreGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("AWS Parameter Store Manager")
        self.root.geometry("1200x800")

        self.manager = AWSParameterManager()
        self.current_parameters = []

        self.setup_gui()

    def setup_gui(self):
        """Setup the GUI components"""
        # Create main notebook for tabs
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Tab 1: Configuration
        self.config_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.config_frame, text="Configuration")
        self.setup_config_tab()

        # Tab 2: Upload Parameters
        self.upload_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.upload_frame, text="Upload Parameters")
        self.setup_upload_tab()

        # Tab 3: View Parameters
        self.view_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.view_frame, text="View Parameters")
        self.setup_view_tab()

        # Status bar
        self.status_var = tk.StringVar()
        self.status_var.set("Ready")
        self.status_bar = ttk.Label(
            self.root, textvariable=self.status_var, relief=tk.SUNKEN
        )
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)

    def setup_config_tab(self):
        """Setup AWS configuration tab"""
        # Create a scrollable frame for the configuration
        canvas = tk.Canvas(self.config_frame)
        scrollbar = ttk.Scrollbar(
            self.config_frame, orient="vertical", command=canvas.yview
        )
        scrollable_frame = ttk.Frame(canvas)

        scrollable_frame.bind(
            "<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        # Authentication Method Selection
        auth_method_frame = ttk.LabelFrame(
            scrollable_frame, text="Authentication Method", padding=10
        )
        auth_method_frame.pack(fill=tk.X, padx=10, pady=5)

        self.auth_method_var = tk.StringVar(value=AuthMethod.ACCESS_KEY.value)
        auth_methods = [
            (AuthMethod.ACCESS_KEY.value, "Access Key & Secret"),
            (AuthMethod.PROFILE.value, "AWS Profile"),
            (AuthMethod.SSO.value, "AWS SSO"),
            (AuthMethod.ROLE.value, "IAM Role Assumption"),
            (AuthMethod.ENVIRONMENT.value, "Environment Variables"),
            (AuthMethod.DEFAULT.value, "Default Credential Chain"),
        ]

        for i, (value, text) in enumerate(auth_methods):
            rb = ttk.Radiobutton(
                auth_method_frame,
                text=text,
                variable=self.auth_method_var,
                value=value,
                command=self.on_auth_method_change,
            )
            rb.grid(row=i // 2, column=i % 2, sticky=tk.W, padx=10, pady=2)

        # Common settings frame
        common_frame = ttk.LabelFrame(
            scrollable_frame, text="Common Settings", padding=10
        )
        common_frame.pack(fill=tk.X, padx=10, pady=5)

        # Region
        ttk.Label(common_frame, text="AWS Region:").grid(
            row=0, column=0, sticky=tk.W, pady=2
        )
        self.region_var = tk.StringVar(value="us-east-1")
        region_combo = ttk.Combobox(
            common_frame, textvariable=self.region_var, width=47
        )
        region_combo["values"] = [
            "us-east-1",
            "us-east-2",
            "us-west-1",
            "us-west-2",
            "eu-west-1",
            "eu-west-2",
            "eu-central-1",
            "ap-southeast-1",
            "ap-southeast-2",
            "ap-northeast-1",
            "ap-south-1",
            "ca-central-1",
        ]
        region_combo.grid(row=0, column=1, sticky=tk.W, padx=(10, 0), pady=2)

        # KMS Key
        ttk.Label(common_frame, text="Default KMS Key:").grid(
            row=1, column=0, sticky=tk.W, pady=2
        )
        self.kms_key_var = tk.StringVar(value="alias/aws/ssm")
        kms_entry = ttk.Entry(common_frame, textvariable=self.kms_key_var, width=50)
        kms_entry.grid(row=1, column=1, sticky=tk.W, padx=(10, 0), pady=2)

        # Access Key Configuration Frame
        self.access_key_frame = ttk.LabelFrame(
            scrollable_frame, text="Access Key Configuration", padding=10
        )
        self.access_key_frame.pack(fill=tk.X, padx=10, pady=5)

        ttk.Label(self.access_key_frame, text="AWS Access Key ID:").grid(
            row=0, column=0, sticky=tk.W, pady=2
        )
        self.access_key_var = tk.StringVar()
        access_key_entry = ttk.Entry(
            self.access_key_frame, textvariable=self.access_key_var, width=50
        )
        access_key_entry.grid(row=0, column=1, sticky=tk.W, padx=(10, 0), pady=2)

        ttk.Label(self.access_key_frame, text="AWS Secret Access Key:").grid(
            row=1, column=0, sticky=tk.W, pady=2
        )
        self.secret_key_var = tk.StringVar()
        secret_key_entry = ttk.Entry(
            self.access_key_frame, textvariable=self.secret_key_var, width=50, show="*"
        )
        secret_key_entry.grid(row=1, column=1, sticky=tk.W, padx=(10, 0), pady=2)

        ttk.Label(self.access_key_frame, text="AWS Session Token (optional):").grid(
            row=2, column=0, sticky=tk.W, pady=2
        )
        self.session_token_var = tk.StringVar()
        session_token_entry = ttk.Entry(
            self.access_key_frame,
            textvariable=self.session_token_var,
            width=50,
            show="*",
        )
        session_token_entry.grid(row=2, column=1, sticky=tk.W, padx=(10, 0), pady=2)

        # Profile Configuration Frame
        self.profile_frame = ttk.LabelFrame(
            scrollable_frame, text="AWS Profile Configuration", padding=10
        )
        self.profile_frame.pack(fill=tk.X, padx=10, pady=5)

        ttk.Label(self.profile_frame, text="Profile Name:").grid(
            row=0, column=0, sticky=tk.W, pady=2
        )
        self.profile_name_var = tk.StringVar()
        profile_entry = ttk.Entry(
            self.profile_frame, textvariable=self.profile_name_var, width=50
        )
        profile_entry.grid(row=0, column=1, sticky=tk.W, padx=(10, 0), pady=2)

        # List available profiles button
        list_profiles_btn = ttk.Button(
            self.profile_frame,
            text="List Available Profiles",
            command=self.list_aws_profiles,
        )
        list_profiles_btn.grid(row=1, column=1, sticky=tk.W, padx=(10, 0), pady=5)

        # SSO Configuration Frame
        self.sso_frame = ttk.LabelFrame(
            scrollable_frame, text="AWS SSO Configuration", padding=10
        )
        self.sso_frame.pack(fill=tk.X, padx=10, pady=5)

        ttk.Label(self.sso_frame, text="SSO Start URL:").grid(
            row=0, column=0, sticky=tk.W, pady=2
        )
        self.sso_start_url_var = tk.StringVar()
        sso_url_entry = ttk.Entry(
            self.sso_frame, textvariable=self.sso_start_url_var, width=50
        )
        sso_url_entry.grid(row=0, column=1, sticky=tk.W, padx=(10, 0), pady=2)

        ttk.Label(self.sso_frame, text="SSO Region:").grid(
            row=1, column=0, sticky=tk.W, pady=2
        )
        self.sso_region_var = tk.StringVar(value="us-east-1")
        sso_region_combo = ttk.Combobox(
            self.sso_frame, textvariable=self.sso_region_var, width=47
        )
        sso_region_combo["values"] = region_combo["values"]
        sso_region_combo.grid(row=1, column=1, sticky=tk.W, padx=(10, 0), pady=2)

        ttk.Label(self.sso_frame, text="Account ID:").grid(
            row=2, column=0, sticky=tk.W, pady=2
        )
        self.sso_account_id_var = tk.StringVar()
        sso_account_entry = ttk.Entry(
            self.sso_frame, textvariable=self.sso_account_id_var, width=50
        )
        sso_account_entry.grid(row=2, column=1, sticky=tk.W, padx=(10, 0), pady=2)

        ttk.Label(self.sso_frame, text="Role Name:").grid(
            row=3, column=0, sticky=tk.W, pady=2
        )
        self.sso_role_name_var = tk.StringVar()
        sso_role_entry = ttk.Entry(
            self.sso_frame, textvariable=self.sso_role_name_var, width=50
        )
        sso_role_entry.grid(row=3, column=1, sticky=tk.W, padx=(10, 0), pady=2)

        # Role Assumption Configuration Frame
        self.role_frame = ttk.LabelFrame(
            scrollable_frame, text="IAM Role Assumption Configuration", padding=10
        )
        self.role_frame.pack(fill=tk.X, padx=10, pady=5)

        ttk.Label(self.role_frame, text="Role ARN:").grid(
            row=0, column=0, sticky=tk.W, pady=2
        )
        self.role_arn_var = tk.StringVar()
        role_arn_entry = ttk.Entry(
            self.role_frame, textvariable=self.role_arn_var, width=50
        )
        role_arn_entry.grid(row=0, column=1, sticky=tk.W, padx=(10, 0), pady=2)

        ttk.Label(self.role_frame, text="Session Name (optional):").grid(
            row=1, column=0, sticky=tk.W, pady=2
        )
        self.role_session_name_var = tk.StringVar()
        role_session_entry = ttk.Entry(
            self.role_frame, textvariable=self.role_session_name_var, width=50
        )
        role_session_entry.grid(row=1, column=1, sticky=tk.W, padx=(10, 0), pady=2)

        ttk.Label(self.role_frame, text="External ID (optional):").grid(
            row=2, column=0, sticky=tk.W, pady=2
        )
        self.external_id_var = tk.StringVar()
        external_id_entry = ttk.Entry(
            self.role_frame, textvariable=self.external_id_var, width=50
        )
        external_id_entry.grid(row=2, column=1, sticky=tk.W, padx=(10, 0), pady=2)

        ttk.Label(self.role_frame, text="MFA Serial (optional):").grid(
            row=3, column=0, sticky=tk.W, pady=2
        )
        self.mfa_serial_var = tk.StringVar()
        mfa_serial_entry = ttk.Entry(
            self.role_frame, textvariable=self.mfa_serial_var, width=50
        )
        mfa_serial_entry.grid(row=3, column=1, sticky=tk.W, padx=(10, 0), pady=2)

        ttk.Label(self.role_frame, text="MFA Token (optional):").grid(
            row=4, column=0, sticky=tk.W, pady=2
        )
        self.mfa_token_var = tk.StringVar()
        mfa_token_entry = ttk.Entry(
            self.role_frame, textvariable=self.mfa_token_var, width=50
        )
        mfa_token_entry.grid(row=4, column=1, sticky=tk.W, padx=(10, 0), pady=2)

        # Environment Variables Info Frame
        self.env_frame = ttk.LabelFrame(
            scrollable_frame, text="Environment Variables Information", padding=10
        )
        self.env_frame.pack(fill=tk.X, padx=10, pady=5)

        env_info_text = """Environment variables that will be used:
• AWS_ACCESS_KEY_ID
• AWS_SECRET_ACCESS_KEY
• AWS_SESSION_TOKEN (optional)
• AWS_DEFAULT_REGION (optional)
• AWS_PROFILE (optional)"""

        env_info_label = ttk.Label(self.env_frame, text=env_info_text, justify=tk.LEFT)
        env_info_label.pack(anchor=tk.W)

        # Default Credential Chain Info Frame
        self.default_frame = ttk.LabelFrame(
            scrollable_frame, text="Default Credential Chain Information", padding=10
        )
        self.default_frame.pack(fill=tk.X, padx=10, pady=5)

        default_info_text = """AWS will search for credentials in this order:
1. Environment variables
2. AWS credentials file (~/.aws/credentials)
3. AWS config file (~/.aws/config)
4. IAM roles for Amazon EC2
5. IAM roles for tasks (ECS)
6. IAM roles for Lambda functions"""

        default_info_label = ttk.Label(
            self.default_frame, text=default_info_text, justify=tk.LEFT
        )
        default_info_label.pack(anchor=tk.W)

        # Connection controls
        connection_frame = ttk.Frame(scrollable_frame)
        connection_frame.pack(fill=tk.X, padx=10, pady=10)

        connect_btn = ttk.Button(
            connection_frame, text="Connect to AWS", command=self.connect_to_aws
        )
        connect_btn.pack(side=tk.LEFT, padx=(0, 10))

        self.connection_status_var = tk.StringVar(value="Not Connected")
        status_label = ttk.Label(
            connection_frame, textvariable=self.connection_status_var, foreground="red"
        )
        status_label.pack(side=tk.LEFT)

        # Pack the canvas and scrollbar
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Initialize the display
        self.on_auth_method_change()

    def setup_upload_tab(self):
        """Setup parameter upload tab"""
        # File selection frame
        file_frame = ttk.LabelFrame(
            self.upload_frame, text="CSV File Selection", padding=10
        )
        file_frame.pack(fill=tk.X, padx=10, pady=5)

        self.csv_file_var = tk.StringVar()
        file_entry = ttk.Entry(file_frame, textvariable=self.csv_file_var, width=60)
        file_entry.pack(side=tk.LEFT, padx=(0, 10))

        browse_btn = ttk.Button(file_frame, text="Browse", command=self.browse_csv_file)
        browse_btn.pack(side=tk.LEFT)

        # CSV format info
        info_frame = ttk.LabelFrame(
            self.upload_frame, text="CSV Format Information", padding=10
        )
        info_frame.pack(fill=tk.X, padx=10, pady=5)

        info_text = """CSV File Format Requirements:
Required columns: key, value, type
Optional columns: tier, kms

Example:
key,value,type,tier,kms
/app/database/host,localhost,String,Standard,
/app/database/password,secretpassword,SecureString,Standard,alias/aws/ssm
/app/features,feature1;feature2,StringList,Standard,

Valid types: String, StringList, SecureString
Valid tiers: Standard, Advanced, Intelligent-Tiering"""

        info_label = ttk.Label(info_frame, text=info_text, justify=tk.LEFT)
        info_label.pack()

        # Upload controls
        upload_frame = ttk.LabelFrame(
            self.upload_frame, text="Upload Parameters", padding=10
        )
        upload_frame.pack(fill=tk.X, padx=10, pady=5)

        self.overwrite_var = tk.BooleanVar()
        overwrite_check = ttk.Checkbutton(
            upload_frame,
            text="Overwrite existing parameters without asking",
            variable=self.overwrite_var,
        )
        overwrite_check.pack(anchor=tk.W, pady=5)

        upload_btn = ttk.Button(
            upload_frame, text="Upload Parameters", command=self.upload_parameters
        )
        upload_btn.pack(pady=5)

        # Upload log
        log_frame = ttk.LabelFrame(self.upload_frame, text="Upload Log", padding=10)
        log_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        self.upload_log = scrolledtext.ScrolledText(log_frame, height=10)
        self.upload_log.pack(fill=tk.BOTH, expand=True)

    def setup_view_tab(self):
        """Setup parameter viewing tab"""
        # Controls frame
        controls_frame = ttk.Frame(self.view_frame)
        controls_frame.pack(fill=tk.X, padx=10, pady=5)

        refresh_btn = ttk.Button(
            controls_frame, text="Refresh Parameters", command=self.refresh_parameters
        )
        refresh_btn.pack(side=tk.LEFT, padx=(0, 10))

        export_btn = ttk.Button(
            controls_frame, text="Export to CSV", command=self.export_parameters
        )
        export_btn.pack(side=tk.LEFT, padx=(0, 10))

        self.decrypt_var = tk.BooleanVar(value=True)
        decrypt_check = ttk.Checkbutton(
            controls_frame,
            text="Decrypt SecureString values",
            variable=self.decrypt_var,
        )
        decrypt_check.pack(side=tk.LEFT, padx=(10, 0))

        # Search frame
        search_frame = ttk.Frame(self.view_frame)
        search_frame.pack(fill=tk.X, padx=10, pady=5)

        ttk.Label(search_frame, text="Search:").pack(side=tk.LEFT)
        self.search_var = tk.StringVar()
        self.search_var.trace("w", self.filter_parameters)
        search_entry = ttk.Entry(search_frame, textvariable=self.search_var, width=30)
        search_entry.pack(side=tk.LEFT, padx=(5, 0))

        # Parameters tree
        tree_frame = ttk.Frame(self.view_frame)
        tree_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        # Create treeview with scrollbars
        self.tree = ttk.Treeview(tree_frame)
        self.tree["columns"] = (
            "Value",
            "Type",
            "Tier",
            "KeyId",
            "LastModified",
            "Version",
        )
        self.tree["show"] = "tree headings"

        # Configure columns
        self.tree.column("#0", width=250, minwidth=200)
        self.tree.column("Value", width=200, minwidth=150)
        self.tree.column("Type", width=100, minwidth=80)
        self.tree.column("Tier", width=100, minwidth=80)
        self.tree.column("KeyId", width=150, minwidth=100)
        self.tree.column("LastModified", width=150, minwidth=120)
        self.tree.column("Version", width=80, minwidth=60)

        # Configure headings
        self.tree.heading("#0", text="Parameter Name", anchor=tk.W)
        self.tree.heading("Value", text="Value", anchor=tk.W)
        self.tree.heading("Type", text="Type", anchor=tk.W)
        self.tree.heading("Tier", text="Tier", anchor=tk.W)
        self.tree.heading("KeyId", text="KMS Key", anchor=tk.W)
        self.tree.heading("LastModified", text="Last Modified", anchor=tk.W)
        self.tree.heading("Version", text="Version", anchor=tk.W)

        # Add scrollbars
        v_scrollbar = ttk.Scrollbar(
            tree_frame, orient=tk.VERTICAL, command=self.tree.yview
        )
        h_scrollbar = ttk.Scrollbar(
            tree_frame, orient=tk.HORIZONTAL, command=self.tree.xview
        )
        self.tree.configure(
            yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set
        )

        # Pack treeview and scrollbars
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        v_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        h_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)

        # Context menu for tree
        self.context_menu = tk.Menu(self.root, tearoff=0)
        self.context_menu.add_command(
            label="Copy Name", command=self.copy_parameter_name
        )
        self.context_menu.add_command(
            label="Copy Value", command=self.copy_parameter_value
        )
        self.context_menu.add_separator()
        self.context_menu.add_command(
            label="Delete Parameter", command=self.delete_selected_parameter
        )

        self.tree.bind("<Button-3>", self.show_context_menu)

    def on_auth_method_change(self):
        """Handle authentication method change"""
        method = AuthMethod(self.auth_method_var.get())

        # Hide all method-specific frames
        self.access_key_frame.pack_forget()
        self.profile_frame.pack_forget()
        self.sso_frame.pack_forget()
        self.role_frame.pack_forget()
        self.env_frame.pack_forget()
        self.default_frame.pack_forget()

        # Show the relevant frame
        if method == AuthMethod.ACCESS_KEY:
            self.access_key_frame.pack(fill=tk.X, padx=10, pady=5)
        elif method == AuthMethod.PROFILE:
            self.profile_frame.pack(fill=tk.X, padx=10, pady=5)
        elif method == AuthMethod.SSO:
            self.sso_frame.pack(fill=tk.X, padx=10, pady=5)
        elif method == AuthMethod.ROLE:
            self.role_frame.pack(fill=tk.X, padx=10, pady=5)
        elif method == AuthMethod.ENVIRONMENT:
            self.env_frame.pack(fill=tk.X, padx=10, pady=5)
        elif method == AuthMethod.DEFAULT:
            self.default_frame.pack(fill=tk.X, padx=10, pady=5)

    def list_aws_profiles(self):
        """List available AWS profiles"""
        try:
            import configparser
            import os

            profiles = []

            # Check AWS credentials file
            creds_file = os.path.expanduser("~/.aws/credentials")
            if os.path.exists(creds_file):
                config = configparser.ConfigParser()
                config.read(creds_file)
                profiles.extend(
                    [section for section in config.sections() if section != "default"]
                )

            # Check AWS config file
            config_file = os.path.expanduser("~/.aws/config")
            if os.path.exists(config_file):
                config = configparser.ConfigParser()
                config.read(config_file)
                for section in config.sections():
                    if section.startswith("profile "):
                        profile_name = section.replace("profile ", "")
                        if profile_name not in profiles:
                            profiles.append(profile_name)

            # Add default profile if credentials file exists
            if os.path.exists(creds_file):
                profiles.insert(0, "default")

            if profiles:
                profile_list = "\\n".join(f"• {profile}" for profile in profiles)
                messagebox.showinfo(
                    "Available AWS Profiles", f"Found profiles:\\n\\n{profile_list}"
                )
            else:
                messagebox.showinfo(
                    "No Profiles Found",
                    "No AWS profiles found. Please configure AWS CLI first.",
                )

        except Exception as e:
            messagebox.showerror("Error", f"Error listing profiles: {str(e)}")

    def connect_to_aws(self):
        """Connect to AWS with configured authentication method"""
        method = AuthMethod(self.auth_method_var.get())

        try:
            # Configure authentication based on selected method
            if method == AuthMethod.ACCESS_KEY:
                if not self.access_key_var.get() or not self.secret_key_var.get():
                    messagebox.showerror(
                        "Error",
                        "Please provide AWS Access Key ID and Secret Access Key",
                    )
                    return

                aws_config.set_access_key_auth(
                    access_key_id=self.access_key_var.get(),
                    secret_access_key=self.secret_key_var.get(),
                    session_token=(
                        self.session_token_var.get()
                        if self.session_token_var.get()
                        else None
                    ),
                    region=self.region_var.get(),
                )

            elif method == AuthMethod.PROFILE:
                if not self.profile_name_var.get():
                    messagebox.showerror("Error", "Please provide AWS Profile Name")
                    return

                aws_config.set_profile_auth(
                    profile_name=self.profile_name_var.get(),
                    region=self.region_var.get(),
                )

            elif method == AuthMethod.SSO:
                if not all(
                    [
                        self.sso_start_url_var.get(),
                        self.sso_region_var.get(),
                        self.sso_account_id_var.get(),
                        self.sso_role_name_var.get(),
                    ]
                ):
                    messagebox.showerror(
                        "Error", "Please provide all SSO configuration details"
                    )
                    return

                aws_config.set_sso_auth(
                    sso_start_url=self.sso_start_url_var.get(),
                    sso_region=self.sso_region_var.get(),
                    sso_account_id=self.sso_account_id_var.get(),
                    sso_role_name=self.sso_role_name_var.get(),
                    region=self.region_var.get(),
                )

            elif method == AuthMethod.ROLE:
                if not self.role_arn_var.get():
                    messagebox.showerror("Error", "Please provide Role ARN")
                    return

                aws_config.set_role_auth(
                    role_arn=self.role_arn_var.get(),
                    role_session_name=(
                        self.role_session_name_var.get()
                        if self.role_session_name_var.get()
                        else None
                    ),
                    external_id=(
                        self.external_id_var.get()
                        if self.external_id_var.get()
                        else None
                    ),
                    mfa_serial=(
                        self.mfa_serial_var.get() if self.mfa_serial_var.get() else None
                    ),
                    mfa_token=(
                        self.mfa_token_var.get() if self.mfa_token_var.get() else None
                    ),
                    region=self.region_var.get(),
                )

            elif method == AuthMethod.ENVIRONMENT:
                aws_config.set_environment_auth(region=self.region_var.get())

            elif method == AuthMethod.DEFAULT:
                aws_config.set_default_auth(region=self.region_var.get())

            # Set KMS key
            aws_config.kms_key_alias = self.kms_key_var.get()

            self.status_var.set("Connecting to AWS...")

            def connect_thread():
                try:
                    if self.manager.connect():
                        auth_info = aws_config.get_auth_info()
                        status_text = (
                            f"Connected ({auth_info['method']} - {auth_info['region']})"
                        )

                        self.root.after(
                            0, lambda: self.connection_status_var.set(status_text)
                        )
                        self.root.after(
                            0, lambda: self.status_var.set("Connected to AWS")
                        )
                        self.root.after(
                            0,
                            lambda: messagebox.showinfo(
                                "Success",
                                f"Successfully connected to AWS\\n\\nMethod: {auth_info['method']}\\nRegion: {auth_info['region']}",
                            ),
                        )
                    else:
                        self.root.after(
                            0,
                            lambda: self.connection_status_var.set("Connection Failed"),
                        )
                        self.root.after(
                            0, lambda: self.status_var.set("Failed to connect to AWS")
                        )
                except Exception as e:
                    error_msg = str(e)
                    self.root.after(
                        0,
                        lambda: messagebox.showerror(
                            "Connection Error", f"Failed to connect: {error_msg}"
                        ),
                    )
                    self.root.after(
                        0, lambda: self.connection_status_var.set("Connection Failed")
                    )
                    self.root.after(0, lambda: self.status_var.set("Ready"))

            threading.Thread(target=connect_thread, daemon=True).start()

        except Exception as e:
            messagebox.showerror(
                "Configuration Error", f"Error configuring authentication: {str(e)}"
            )

    def browse_csv_file(self):
        """Browse and select CSV file"""
        filename = filedialog.askopenfilename(
            title="Select CSV file",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
        )
        if filename:
            self.csv_file_var.set(filename)

    def upload_parameters(self):
        """Upload parameters from CSV file"""
        if not self.manager.ssm_client:
            messagebox.showerror("Error", "Please connect to AWS first")
            return

        if not self.csv_file_var.get():
            messagebox.showerror("Error", "Please select a CSV file")
            return

        def upload_thread():
            try:
                self.root.after(0, lambda: self.status_var.set("Reading CSV file..."))
                parameters = self.manager.read_csv_parameters(self.csv_file_var.get())

                if not parameters:
                    self.root.after(
                        0,
                        lambda: messagebox.showwarning(
                            "Warning", "No valid parameters found in CSV file"
                        ),
                    )
                    return

                self.root.after(0, lambda: self.upload_log.delete("1.0", tk.END))
                self.root.after(
                    0,
                    lambda: self.log_message(
                        f"Found {len(parameters)} parameters to upload\\n"
                    ),
                )

                uploaded_count = 0
                skipped_count = 0

                for i, param in enumerate(parameters):
                    self.root.after(
                        0,
                        lambda p=param: self.status_var.set(
                            f"Processing {p['key']}..."
                        ),
                    )

                    # Check if parameter exists
                    exists, existing_param = self.manager.parameter_exists(param["key"])

                    if exists and not self.overwrite_var.get():
                        self.root.after(
                            0,
                            lambda p=param, ep=existing_param: self.log_message(
                                f"Parameter {p['key']} already exists:\\n"
                                f"  Current: {ep['Value'][:50]}{'...' if len(ep['Value']) > 50 else ''}\\n"
                                f"  New: {p['value'][:50]}{'...' if len(p['value']) > 50 else ''}\\n"
                            ),
                        )

                        # Ask user for confirmation
                        result = messagebox.askyesnocancel(
                            "Parameter Exists",
                            f"Parameter '{param['key']}' already exists.\\n\\n"
                            f"Current value: {existing_param['Value'][:100]}{'...' if len(existing_param['Value']) > 100 else ''}\\n"
                            f"New value: {param['value'][:100]}{'...' if len(param['value']) > 100 else ''}\\n\\n"
                            f"Do you want to replace it?",
                            title="Replace Parameter",
                        )

                        if result is None:  # Cancel
                            self.root.after(
                                0,
                                lambda: self.log_message("Upload cancelled by user\\n"),
                            )
                            break
                        elif not result:  # No
                            skipped_count += 1
                            self.root.after(
                                0,
                                lambda p=param: self.log_message(
                                    f"Skipped {p['key']}\\n"
                                ),
                            )
                            continue
                        # Yes - continue with upload

                    # Upload parameter
                    if self.manager.create_or_update_parameter(param, overwrite=True):
                        uploaded_count += 1
                        self.root.after(
                            0,
                            lambda p=param: self.log_message(
                                f"✓ Uploaded {p['key']}\\n"
                            ),
                        )
                    else:
                        self.root.after(
                            0,
                            lambda p=param: self.log_message(
                                f"✗ Failed to upload {p['key']}\\n"
                            ),
                        )

                self.root.after(
                    0,
                    lambda: self.log_message(
                        f"\\nUpload completed: {uploaded_count} uploaded, {skipped_count} skipped\\n"
                    ),
                )
                self.root.after(
                    0,
                    lambda: self.status_var.set(
                        f"Upload completed: {uploaded_count} uploaded, {skipped_count} skipped"
                    ),
                )

            except Exception as e:
                error_msg = str(e)
                self.root.after(
                    0,
                    lambda: messagebox.showerror(
                        "Upload Error", f"Error during upload: {error_msg}"
                    ),
                )
                self.root.after(0, lambda: self.status_var.set("Upload failed"))

        threading.Thread(target=upload_thread, daemon=True).start()

    def log_message(self, message):
        """Add message to upload log"""
        self.upload_log.insert(tk.END, message)
        self.upload_log.see(tk.END)

    def refresh_parameters(self):
        """Refresh parameter list"""
        if not self.manager.ssm_client:
            messagebox.showerror("Error", "Please connect to AWS first")
            return

        def refresh_thread():
            try:
                self.root.after(
                    0, lambda: self.status_var.set("Refreshing parameters...")
                )
                parameters = self.manager.get_all_parameters(
                    decrypt=self.decrypt_var.get()
                )
                self.current_parameters = parameters

                self.root.after(0, lambda: self.populate_tree(parameters))
                self.root.after(
                    0,
                    lambda: self.status_var.set(f"Loaded {len(parameters)} parameters"),
                )

            except Exception as e:
                error_msg = str(e)
                self.root.after(
                    0,
                    lambda: messagebox.showerror(
                        "Refresh Error", f"Error refreshing parameters: {error_msg}"
                    ),
                )
                self.root.after(0, lambda: self.status_var.set("Refresh failed"))

        threading.Thread(target=refresh_thread, daemon=True).start()

    def populate_tree(self, parameters):
        """Populate the parameters tree"""
        # Clear existing items
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Add parameters to tree
        for param in parameters:
            # Truncate long values for display
            display_value = param["Value"]
            if len(display_value) > 100:
                display_value = display_value[:97] + "..."

            # Format last modified date
            last_modified = param.get("LastModifiedDate", "")
            if last_modified:
                if hasattr(last_modified, "strftime"):
                    last_modified = last_modified.strftime("%Y-%m-%d %H:%M:%S")
                else:
                    last_modified = str(last_modified)

            self.tree.insert(
                "",
                tk.END,
                text=param["Name"],
                values=(
                    display_value,
                    param["Type"],
                    param.get("Tier", ""),
                    param.get("KeyId", ""),
                    last_modified,
                    param.get("Version", ""),
                ),
            )

    def filter_parameters(self, *args):
        """Filter parameters based on search text"""
        search_text = self.search_var.get().lower()

        if not search_text:
            self.populate_tree(self.current_parameters)
            return

        filtered_params = [
            param
            for param in self.current_parameters
            if search_text in param["Name"].lower()
            or search_text in param["Value"].lower()
        ]

        self.populate_tree(filtered_params)

    def show_context_menu(self, event):
        """Show context menu for tree item"""
        item = self.tree.identify_row(event.y)
        if item:
            self.tree.selection_set(item)
            self.context_menu.post(event.x_root, event.y_root)

    def copy_parameter_name(self):
        """Copy selected parameter name to clipboard"""
        selected = self.tree.selection()
        if selected:
            item = selected[0]
            name = self.tree.item(item, "text")
            self.root.clipboard_clear()
            self.root.clipboard_append(name)
            self.status_var.set(f"Copied parameter name: {name}")

    def copy_parameter_value(self):
        """Copy selected parameter value to clipboard"""
        selected = self.tree.selection()
        if selected:
            item = selected[0]
            name = self.tree.item(item, "text")

            # Find the full parameter to get complete value
            param = next(
                (p for p in self.current_parameters if p["Name"] == name), None
            )
            if param:
                self.root.clipboard_clear()
                self.root.clipboard_append(param["Value"])
                self.status_var.set(f"Copied parameter value for: {name}")

    def delete_selected_parameter(self):
        """Delete selected parameter"""
        selected = self.tree.selection()
        if selected:
            item = selected[0]
            name = self.tree.item(item, "text")

            result = messagebox.askyesno(
                "Delete Parameter",
                f"Are you sure you want to delete parameter '{name}'?\\n\\nThis action cannot be undone.",
                icon="warning",
            )

            if result:

                def delete_thread():
                    try:
                        if self.manager.delete_parameter(name):
                            self.root.after(0, lambda: self.tree.delete(item))
                            self.root.after(
                                0,
                                lambda: self.status_var.set(
                                    f"Deleted parameter: {name}"
                                ),
                            )
                            # Remove from current_parameters list
                            self.current_parameters = [
                                p for p in self.current_parameters if p["Name"] != name
                            ]
                        else:
                            self.root.after(
                                0,
                                lambda: messagebox.showerror(
                                    "Delete Error",
                                    f"Failed to delete parameter: {name}",
                                ),
                            )
                    except Exception as e:
                        error_msg = str(e)
                        self.root.after(
                            0,
                            lambda: messagebox.showerror(
                                "Delete Error", f"Error deleting parameter: {error_msg}"
                            ),
                        )

                threading.Thread(target=delete_thread, daemon=True).start()

    def export_parameters(self):
        """Export current parameters to CSV"""
        if not self.current_parameters:
            messagebox.showwarning(
                "Warning", "No parameters to export. Please refresh first."
            )
            return

        filename = filedialog.asksaveasfilename(
            title="Export parameters to CSV",
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
        )

        if filename:
            if self.manager.export_parameters_to_csv(filename, self.current_parameters):
                messagebox.showinfo("Success", f"Parameters exported to {filename}")
                self.status_var.set(
                    f"Exported {len(self.current_parameters)} parameters to CSV"
                )
            else:
                messagebox.showerror("Error", "Failed to export parameters")


def main():
    root = tk.Tk()
    app = ParameterStoreGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
