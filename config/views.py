from django.http import HttpResponse


def home(request):
    return HttpResponse("""
        <h1>Welcome to Job Portal Backend API</h1>
        <p>This is a production-level Django + DRF backend project.</p>
        <p>Available APIs:</p>
        <ul>
            <li>/api/accounts/</li>
            <li>/api/jobs/</li>
            <li>/api/applications/</li>
            <li>/api/interviews/</li>
            <li>/api/token/</li>
        </ul>
    """)