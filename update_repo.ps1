# Скрипт для обновления репозитория
Write-Host " Обновляю репозиторий malika-s1/TaskFlowPlus..." -ForegroundColor Cyan

# Добавляем все изменения
git add .

# Коммит с текущей датой
$date = Get-Date -Format "yyyy-MM-dd HH:mm"
git commit -m "Update: $date

- Project maintenance
- Code improvements
- Documentation updates"

# Пушим на GitHub
git push origin main

Write-Host " Репозиторий успешно обновлен!" -ForegroundColor Green
Write-Host " https://github.com/malika-s1/TaskFlowPlus" -ForegroundColor Yellow
