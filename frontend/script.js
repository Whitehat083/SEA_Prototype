document.addEventListener('DOMContentLoaded', () => {
    const BASE_LOCATION = [40.7128, -74.0060];
    const API_URL = 'http://localhost:8000';
    const WS_URL = 'ws://localhost:8000/ws'; // URL explícita para o WebSocket

    const map = L.map('map').setView(BASE_LOCATION, 14);
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '© <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
    }).addTo(map);

    let droneMarkers = {};
    let lastDroneStatus = {};
    let targetMarker = null;
    const logPanel = document.getElementById('log-panel');
    
    function logEvent(message, level = 'info') {
        const entry = document.createElement('div');
        entry.className = `log-entry log-${level}`;
        entry.textContent = `[${new Date().toLocaleTimeString()}] ${message}`;
        logPanel.appendChild(entry);
        logPanel.scrollTop = logPanel.scrollHeight;
    }

    // --- Lógica de Conexão WebSocket (COM DIAGNÓSTICO) ---
    function connect() {
        console.log(`Frontend: Tentando conectar ao WebSocket em ${WS_URL}`);
        logEvent(`Tentando conectar ao servidor...`, "info");
        const socket = new WebSocket(WS_URL);

        socket.onopen = (event) => {
            console.log("Frontend: Conexão WebSocket ESTABELECIDA.", event);
            logEvent("Conectado à Plataforma SEA.", "info");
        };

        socket.onclose = (event) => {
            console.error("Frontend: Conexão WebSocket FECHADA.", event);
            if (event.wasClean) {
                logEvent(`Conexão fechada limpiamente, código=${event.code} motivo=${event.reason}`, "warning");
            } else {
                logEvent("Conexão perdida. Tentando reconectar em 5 segundos...", "alert");
                setTimeout(connect, 5000);
            }
        };

        socket.onerror = (error) => {
            console.error("Frontend: ERRO na conexão WebSocket.", error);
            logEvent("Falha ao conectar. O servidor está rodando?", "alert");
        };
        
        socket.onmessage = (event) => {
            const swarmStatus = JSON.parse(event.data);
            updateSwarmUI(swarmStatus);
        };
    }

    // --- Funções de UI (sem alterações) ---
    function updateSwarmUI(swarmStatus) {
        const droneList = document.getElementById('drone-list');
        droneList.innerHTML = ''; 
        
        swarmStatus.forEach(drone => {
            if (lastDroneStatus[drone.id] && lastDroneStatus[drone.id] !== drone.status) {
                const level = ['Offline', 'Comms_Lost'].includes(drone.status) ? 'warning' : 'info';
                logEvent(`${drone.id} status alterado: ${lastDroneStatus[drone.id]} -> ${drone.status}`, level);
            }
            lastDroneStatus[drone.id] = drone.status;
            
            const listItem = document.createElement('li');
            listItem.className = `status-${drone.status}`;
            listItem.innerHTML = `<strong>${drone.id}</strong> | Status: ${drone.status} | Bat: ${drone.battery}%`;
            droneList.appendChild(listItem);

            const isOffline = drone.status === 'Offline';
            if (droneMarkers[drone.id] && isOffline) {
                map.removeLayer(droneMarkers[drone.id]);
                delete droneMarkers[drone.id];
            } else if (!isOffline) {
                const icon = L.icon({iconUrl: 'https://cdn-icons-png.flaticon.com/64/3115/3115174.png', iconSize: [24, 24]});
                if (droneMarkers[drone.id]) {
                    droneMarkers[drone.id].setLatLng(drone.position);
                } else {
                    droneMarkers[drone.id] = L.marker(drone.position, { icon }).addTo(map)
                        .bindPopup(`<b>${drone.id}</b>`);
                }
            }
        });
    }

    map.on('contextmenu', (e) => {
        const targetCoords = [e.latlng.lat, e.latlng.lng];
        logEvent(`Novo alvo GO-TO definido em [${targetCoords[0].toFixed(4)}, ${targetCoords[1].toFixed(4)}]`, 'info');
        const targetIcon = L.icon({iconUrl: 'https://cdn-icons-png.flaticon.com/64/446/446152.png', iconSize: [32, 32]});
        if (targetMarker) {
            targetMarker.setLatLng(targetCoords);
        } else {
            targetMarker = L.marker(targetCoords, {icon: targetIcon}).addTo(map).bindPopup("Alvo do Enxame");
        }
        fetch(`${API_URL}/api/command/go_to_all`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ coordinates: targetCoords })
        });
    });

    document.getElementById('takeoff-btn').addEventListener('click', () => {
        logEvent("Comando DECOLAR ENXAME enviado.", 'alert');
        fetch(`${API_URL}/api/command/takeoff_all`, { method: 'POST' });
    });

    document.getElementById('land-btn').addEventListener('click', () => {
        logEvent("Comando POUSAR ENXAME enviado.", 'alert');
        fetch(`${API_URL}/api/command/land_all`, { method: 'POST' });
    });
    
    // Inicia a primeira tentativa de conexão
    connect();
});