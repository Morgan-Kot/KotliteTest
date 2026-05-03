# KOTLITE BROWSER LAUNCHER
> A streamlined deployment hub for the Kotlite ecosystem.

---

### [ OVERVIEW ]
Kotlite Launcher is a high-performance management utility built to bridge the gap between GitHub releases and your local desktop. It eliminates the hassle of manual updates by providing a one-click interface for version control and browser deployment.

### [ CORE CAPABILITIES ]

*   **SMART SYNC**
    Connects directly to the GitHub API to fetch real-time release data.
    
*   **HYBRID STORAGE**
    Intelligently identifies which versions are in the "Cloud" versus those "Installed" on your local hardware.
    
*   **ASYNCHRONOUS ENGINE**
    Leverages multithreading for background downloads, ensuring the UI remains fluid and responsive.
    
*   **CLEANUP TOOLS**
    Integrated file management allows you to purge old versions with a single click.

---

### [ TECHNICAL STACK ]


| Component      | Specification                     |
| :---           | :---                              |
| **UI Engine**  | CustomTkinter (Dark Mode)         |
| **Logic**      | Python 3.x                        |
| **Network**    | Requests + GitHub REST API        |
| **Paths**      | %APPDATA%/KotliteBrowser/versions |

---

### [ USER GUIDE ]

#### 1. Discovery
Upon startup, the launcher scans the repository. Available versions appear in the **Installations** sidebar.

#### 2. Deployment
*   **CLOUD STATUS:** Click the blue **Install** button to pull the binary from the server.
*   **INSTALLED STATUS:** Click the green **Launch** button to initialize the browser.

#### 3. Execution
When you hit Launch, the launcher handles the subprocess initialization and exits automatically to keep your workspace decluttered.

---

### [ DIRECTORY STRUCTURE ]

```text
AppData/
└── Roaming/
    └── KotliteBrowser/
        ├── versions/
        │   ├── v1.0.exe
        │   └── v1.1.exe
        └── debug.log
```

---

### [ DEVELOPMENT ]
**Author:** Morgan-Kot  
**Platform:** Windows 10 / 11  
**License:** MIT Open Source  

---
