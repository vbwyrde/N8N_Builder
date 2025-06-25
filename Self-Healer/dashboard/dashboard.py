"""
Self-Healer Dashboard - Web-based monitoring interface.

This module provides a web-based dashboard for monitoring the Self-Healer
system's activities, metrics, and health status.
"""

import asyncio
import json
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
from pathlib import Path

from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import uvicorn

# Import existing N8N Builder components
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

from n8n_builder.logging_config import get_logger
from Self_Healer.core.healer_manager import SelfHealerManager


class SelfHealerDashboard:
    """
    Web-based dashboard for monitoring the Self-Healer system.
    
    Features:
    - Real-time system status monitoring
    - Healing session tracking
    - Performance metrics visualization
    - Learning system insights
    - Manual control interface
    """
    
    def __init__(self, healer_manager: SelfHealerManager, port: int = 8081):
        """Initialize the dashboard."""
        self.logger = get_logger('self_healer.dashboard')
        self.healer_manager = healer_manager
        self.port = port
        
        # FastAPI app
        self.app = FastAPI(title="Self-Healer Dashboard", version="1.0.0")
        
        # WebSocket connections for real-time updates
        self.websocket_connections: List[WebSocket] = []
        
        # Dashboard data cache
        self.dashboard_data: Dict[str, Any] = {}
        self.last_update = datetime.now()
        
        # Setup routes
        self._setup_routes()
        
        # Background tasks
        self.update_task: Optional[asyncio.Task] = None
        self.is_running = False
        
        self.logger.info(f"Self-Healer Dashboard initialized on port {port}")
    
    def _setup_routes(self):
        """Setup FastAPI routes."""
        
        @self.app.get("/", response_class=HTMLResponse)
        async def dashboard_home(request: Request):
            """Main dashboard page."""
            return self._get_dashboard_html()
        
        @self.app.get("/api/status")
        async def get_status():
            """Get current system status."""
            try:
                status = await self.healer_manager.get_status()
                return JSONResponse(content=status)
            except Exception as e:
                self.logger.error(f"Error getting status: {e}")
                return JSONResponse(content={"error": str(e)}, status_code=500)
        
        @self.app.get("/api/metrics")
        async def get_metrics():
            """Get system metrics."""
            try:
                metrics = await self._get_comprehensive_metrics()
                return JSONResponse(content=metrics)
            except Exception as e:
                self.logger.error(f"Error getting metrics: {e}")
                return JSONResponse(content={"error": str(e)}, status_code=500)
        
        @self.app.get("/api/sessions")
        async def get_sessions():
            """Get healing sessions."""
            try:
                sessions = await self._get_session_data()
                return JSONResponse(content=sessions)
            except Exception as e:
                self.logger.error(f"Error getting sessions: {e}")
                return JSONResponse(content={"error": str(e)}, status_code=500)
        
        @self.app.get("/api/learning")
        async def get_learning_data():
            """Get learning system data."""
            try:
                learning_data = self.healer_manager.learning_engine.get_learning_statistics()
                return JSONResponse(content=learning_data)
            except Exception as e:
                self.logger.error(f"Error getting learning data: {e}")
                return JSONResponse(content={"error": str(e)}, status_code=500)
        
        @self.app.post("/api/emergency_stop")
        async def emergency_stop():
            """Emergency stop the healing system."""
            try:
                await self.healer_manager.emergency_stop()
                return JSONResponse(content={"status": "emergency_stop_activated"})
            except Exception as e:
                self.logger.error(f"Error during emergency stop: {e}")
                return JSONResponse(content={"error": str(e)}, status_code=500)
        
        @self.app.websocket("/ws")
        async def websocket_endpoint(websocket: WebSocket):
            """WebSocket endpoint for real-time updates."""
            await self._handle_websocket(websocket)
    
    def _get_dashboard_html(self) -> str:
        """Generate dashboard HTML."""
        return """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Self-Healer Dashboard</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 0; padding: 20px; background-color: #f5f5f5; }
        .container { max-width: 1200px; margin: 0 auto; }
        .header { background: #2c3e50; color: white; padding: 20px; border-radius: 8px; margin-bottom: 20px; }
        .metrics-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 20px; margin-bottom: 20px; }
        .metric-card { background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
        .metric-value { font-size: 2em; font-weight: bold; color: #3498db; }
        .metric-label { color: #7f8c8d; margin-top: 5px; }
        .status-indicator { display: inline-block; width: 12px; height: 12px; border-radius: 50%; margin-right: 8px; }
        .status-running { background-color: #27ae60; }
        .status-stopped { background-color: #e74c3c; }
        .status-warning { background-color: #f39c12; }
        .sessions-table { width: 100%; border-collapse: collapse; background: white; border-radius: 8px; overflow: hidden; }
        .sessions-table th, .sessions-table td { padding: 12px; text-align: left; border-bottom: 1px solid #ecf0f1; }
        .sessions-table th { background-color: #34495e; color: white; }
        .emergency-button { background-color: #e74c3c; color: white; border: none; padding: 10px 20px; border-radius: 4px; cursor: pointer; font-size: 16px; }
        .emergency-button:hover { background-color: #c0392b; }
        .section { background: white; padding: 20px; border-radius: 8px; margin-bottom: 20px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
        .section h2 { margin-top: 0; color: #2c3e50; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>Self-Healer Dashboard</h1>
            <p>Real-time monitoring of the N8N Builder Self-Healing System</p>
            <div id="system-status">
                <span class="status-indicator status-running"></span>
                <span>System Status: <span id="status-text">Loading...</span></span>
            </div>
        </div>
        
        <div class="metrics-grid">
            <div class="metric-card">
                <div class="metric-value" id="total-errors">-</div>
                <div class="metric-label">Total Errors Detected</div>
            </div>
            <div class="metric-card">
                <div class="metric-value" id="success-rate">-</div>
                <div class="metric-label">Success Rate</div>
            </div>
            <div class="metric-card">
                <div class="metric-value" id="active-sessions">-</div>
                <div class="metric-label">Active Sessions</div>
            </div>
            <div class="metric-card">
                <div class="metric-value" id="avg-healing-time">-</div>
                <div class="metric-label">Avg Healing Time (s)</div>
            </div>
        </div>
        
        <div class="section">
            <h2>Recent Healing Sessions</h2>
            <table class="sessions-table" id="sessions-table">
                <thead>
                    <tr>
                        <th>Session ID</th>
                        <th>Error Type</th>
                        <th>Status</th>
                        <th>Duration</th>
                        <th>Success</th>
                    </tr>
                </thead>
                <tbody id="sessions-tbody">
                    <tr><td colspan="5">Loading...</td></tr>
                </tbody>
            </table>
        </div>
        
        <div class="section">
            <h2>Learning System</h2>
            <div class="metrics-grid">
                <div class="metric-card">
                    <div class="metric-value" id="total-patterns">-</div>
                    <div class="metric-label">Total Patterns</div>
                </div>
                <div class="metric-card">
                    <div class="metric-value" id="learning-records">-</div>
                    <div class="metric-label">Learning Records</div>
                </div>
                <div class="metric-card">
                    <div class="metric-value" id="effectiveness-score">-</div>
                    <div class="metric-label">Avg Effectiveness</div>
                </div>
            </div>
        </div>
        
        <div class="section">
            <h2>System Controls</h2>
            <button class="emergency-button" onclick="emergencyStop()">Emergency Stop</button>
            <p><small>Use emergency stop only in critical situations. This will halt all healing activities.</small></p>
        </div>
    </div>
    
    <script>
        let ws = null;
        
        function connectWebSocket() {
            const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
            ws = new WebSocket(`${protocol}//${window.location.host}/ws`);
            
            ws.onmessage = function(event) {
                const data = JSON.parse(event.data);
                updateDashboard(data);
            };
            
            ws.onclose = function() {
                setTimeout(connectWebSocket, 5000); // Reconnect after 5 seconds
            };
        }
        
        function updateDashboard(data) {
            if (data.status) {
                document.getElementById('status-text').textContent = data.status.status;
                document.getElementById('total-errors').textContent = data.status.metrics.total_errors_detected;
                document.getElementById('success-rate').textContent = data.status.metrics.success_rate.toFixed(1) + '%';
                document.getElementById('active-sessions').textContent = data.status.active_sessions;
                document.getElementById('avg-healing-time').textContent = data.status.metrics.average_healing_time.toFixed(1);
                
                // Update status indicator
                const indicator = document.querySelector('.status-indicator');
                indicator.className = 'status-indicator ' + (data.status.is_running ? 'status-running' : 'status-stopped');
            }
            
            if (data.sessions) {
                updateSessionsTable(data.sessions);
            }
            
            if (data.learning) {
                document.getElementById('total-patterns').textContent = data.learning.total_patterns;
                document.getElementById('learning-records').textContent = data.learning.total_learning_records;
                document.getElementById('effectiveness-score').textContent = data.learning.average_effectiveness_score.toFixed(2);
            }
        }
        
        function updateSessionsTable(sessions) {
            const tbody = document.getElementById('sessions-tbody');
            tbody.innerHTML = '';
            
            if (sessions.length === 0) {
                tbody.innerHTML = '<tr><td colspan="5">No recent sessions</td></tr>';
                return;
            }
            
            sessions.forEach(session => {
                const row = tbody.insertRow();
                row.innerHTML = `
                    <td>${session.session_id.substring(0, 12)}...</td>
                    <td>${session.error_id}</td>
                    <td>${session.status}</td>
                    <td>${session.duration.toFixed(1)}s</td>
                    <td>${session.success ? '✅' : '❌'}</td>
                `;
            });
        }
        
        async function emergencyStop() {
            if (confirm('Are you sure you want to perform an emergency stop? This will halt all healing activities.')) {
                try {
                    const response = await fetch('/api/emergency_stop', { method: 'POST' });
                    const result = await response.json();
                    alert('Emergency stop activated');
                } catch (error) {
                    alert('Error during emergency stop: ' + error.message);
                }
            }
        }
        
        // Initialize dashboard
        connectWebSocket();
        
        // Periodic updates as fallback
        setInterval(async () => {
            try {
                const [statusResponse, learningResponse] = await Promise.all([
                    fetch('/api/status'),
                    fetch('/api/learning')
                ]);
                
                const status = await statusResponse.json();
                const learning = await learningResponse.json();
                
                updateDashboard({ status, learning });
            } catch (error) {
                console.error('Error updating dashboard:', error);
            }
        }, 10000); // Update every 10 seconds
    </script>
</body>
</html>
        """
    
    async def _handle_websocket(self, websocket: WebSocket):
        """Handle WebSocket connection."""
        await websocket.accept()
        self.websocket_connections.append(websocket)
        
        try:
            while True:
                # Send periodic updates
                await asyncio.sleep(5)
                
                # Get current data
                data = await self._get_dashboard_data()
                await websocket.send_text(json.dumps(data))
                
        except WebSocketDisconnect:
            self.websocket_connections.remove(websocket)
        except Exception as e:
            self.logger.error(f"WebSocket error: {e}")
            if websocket in self.websocket_connections:
                self.websocket_connections.remove(websocket)
    
    async def _get_dashboard_data(self) -> Dict[str, Any]:
        """Get comprehensive dashboard data."""
        try:
            status = await self.healer_manager.get_status()
            learning_stats = self.healer_manager.learning_engine.get_learning_statistics()
            sessions = await self._get_session_data()
            
            return {
                'status': status,
                'learning': learning_stats,
                'sessions': sessions,
                'timestamp': datetime.now().isoformat()
            }
        except Exception as e:
            self.logger.error(f"Error getting dashboard data: {e}")
            return {'error': str(e)}
    
    async def _get_comprehensive_metrics(self) -> Dict[str, Any]:
        """Get comprehensive system metrics."""
        status = await self.healer_manager.get_status()
        learning_stats = self.healer_manager.learning_engine.get_learning_statistics()
        
        return {
            'system_metrics': status['metrics'],
            'learning_metrics': learning_stats,
            'timestamp': datetime.now().isoformat()
        }
    
    async def _get_session_data(self) -> List[Dict[str, Any]]:
        """Get healing session data."""
        status = await self.healer_manager.get_status()
        return status.get('recent_sessions', [])
    
    async def start(self):
        """Start the dashboard server."""
        if self.is_running:
            self.logger.warning("Dashboard is already running")
            return
        
        self.is_running = True
        
        # Start background update task
        self.update_task = asyncio.create_task(self._background_updates())
        
        # Start the web server
        config = uvicorn.Config(
            app=self.app,
            host="0.0.0.0",
            port=self.port,
            log_level="info"
        )
        server = uvicorn.Server(config)
        
        self.logger.info(f"Starting Self-Healer Dashboard on http://localhost:{self.port}")
        await server.serve()
    
    async def stop(self):
        """Stop the dashboard server."""
        if not self.is_running:
            return
        
        self.is_running = False
        
        # Stop background task
        if self.update_task:
            self.update_task.cancel()
            try:
                await self.update_task
            except asyncio.CancelledError:
                pass
        
        # Close WebSocket connections
        for ws in self.websocket_connections:
            try:
                await ws.close()
            except:
                pass
        
        self.websocket_connections.clear()
        self.logger.info("Self-Healer Dashboard stopped")
    
    async def _background_updates(self):
        """Background task for periodic updates."""
        while self.is_running:
            try:
                # Update dashboard data
                self.dashboard_data = await self._get_dashboard_data()
                self.last_update = datetime.now()
                
                # Send updates to connected WebSocket clients
                if self.websocket_connections:
                    message = json.dumps(self.dashboard_data)
                    disconnected = []
                    
                    for ws in self.websocket_connections:
                        try:
                            await ws.send_text(message)
                        except:
                            disconnected.append(ws)
                    
                    # Remove disconnected clients
                    for ws in disconnected:
                        self.websocket_connections.remove(ws)
                
                await asyncio.sleep(5)  # Update every 5 seconds
                
            except asyncio.CancelledError:
                break
            except Exception as e:
                self.logger.error(f"Error in background updates: {e}")
                await asyncio.sleep(10)  # Wait longer on error


async def run_dashboard(healer_manager: SelfHealerManager, port: int = 8081):
    """Run the Self-Healer Dashboard."""
    dashboard = SelfHealerDashboard(healer_manager, port)
    await dashboard.start()
