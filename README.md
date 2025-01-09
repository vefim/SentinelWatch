# SentinelWatch: Real-Time File Integrity Monitoring System  

## Introduction  

SentinelWatch is a real-time file integrity monitoring (FIM) solution designed to track file changes, maintain system integrity, and alert users to potential security threats or performance anomalies.  

The project was originally conceptualized, developed, and implemented by **Victor Efimba** as part of his Senior Project at the University of the District of Columbia's Department of Computer Science and Information Technology. 
Recognizing its potential for broader application, **Soliyana Seyoum** and **Thirno Sow** later joined the effort, contributing key features and optimizations that enhanced its functionality and usability.  

SentinelWatch provides a comprehensive, user-friendly platform for detecting unauthorized file changes, analyzing file activity, and monitoring system performance, empowering organizations to strengthen their cybersecurity posture.  

---

## Key Features  

- **Real-Time File Integrity Monitoring**: Tracks directory changes using the Watchdog library and validates file integrity with SHA-256 hashing.  
- **Z-Score Based File Analytics**: Detects file size anomalies using statistical analysis to identify potential security concerns.  
- **Real-Time Alerts**: Generates immediate alerts for hash mismatches or anomalous file sizes, displayed dynamically on the dashboard.  
- **System Health Monitoring**: Tracks CPU usage, memory consumption, and disk I/O metrics using the psutil library.  
- **File Activity Analytics**: Categorizes files and tracks their activity to provide insights into file usage patterns.  
- **User-Friendly Dashboard**: Features a dynamic interface for visualizing real-time monitoring data, system health, and file activity analytics.  

---

## Technology Stack  

- **Backend**: Python, Flask  
- **Libraries**: Watchdog, psutil  
- **Frontend**: HTML, CSS, JavaScript, AJAX  

---

## Usage

1. **Configure Directory to Monitor**  
   Specify the directory you want to monitor in the configuration file.

2. **Start the Application**  
   Launch the application to begin real-time monitoring of file changes and system performance.

3. **Dashboard**  
   View live system health metrics and file activity through an intuitive dashboard.

4. **Alerts**  
   Respond to alerts for file integrity issues or system performance concerns, ensuring your system runs smoothly.

## Contributions

Contributions are welcome! Please fork the repository, make your changes, and create a pull request. We appreciate your contributions and feedback.

## Acknowledgements

- Special thanks to **Professor Yu** from the University of the District of Columbia for his recommendations and support.
- Open-source libraries used in this project:
  - [Watchdog](https://pypi.org/project/watchdog/) for file monitoring.
  - [psutil](https://pypi.org/project/psutil/) for system health metrics.
