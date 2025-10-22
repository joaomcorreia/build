# Build Platform Development Aliases
# Add these lines to your PowerShell profile for easy access

# Quick development server aliases
function Start-BuildServer { 
    Set-Location "C:\projects\build\build"
    .\dev.bat 
}

function Start-BuildShell { 
    Set-Location "C:\projects\build\build"
    .\dev.bat shell
}

function Start-BuildMigrate { 
    Set-Location "C:\projects\build\build"
    .\dev.bat migrate
}

# Create short aliases
Set-Alias build Start-BuildServer
Set-Alias buildshell Start-BuildShell
Set-Alias buildmigrate Start-BuildMigrate

Write-Host "✅ Build Platform aliases loaded!" -ForegroundColor Green
Write-Host "   build         - Start development server" -ForegroundColor Yellow
Write-Host "   buildshell    - Django shell" -ForegroundColor Yellow  
Write-Host "   buildmigrate  - Run migrations" -ForegroundColor Yellow