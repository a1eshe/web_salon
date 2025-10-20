document.addEventListener('DOMContentLoaded', function() {
    const calendarEl = document.getElementById('calendar');
    
    const calendar = new FullCalendar.Calendar(calendarEl, {
        initialView: 'dayGridMonth',
        events: window.bookingsData,
        eventClick: function(info) {
            const data = info.event.extendedProps;
            alert(
                "👤 Username: " + data.username + "\n" +
                "📱 Tel: " + data.phone + "\n" +
                "✉️ Email: " + data.email + "\n" +
                "🏠 Manzil: " + data.address + "\n" +
                "🎟 Referral code: " + data.referral_code + "\n" +
                "💸 Chegirma: " + data.discount + "%"
            );
        }
    });

    calendar.render();
});