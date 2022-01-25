from rest_framework.permissions import IsAdminUser

class LibrariansOnly(IsAdminUser):
    def has_permission(self, request, view):
        if(request.method=="GET"):
            return True
        isadmin = super().has_permission(request, view)
        islibrarian = request.user.groups.filter(name='Librarians').exists()
        return (islibrarian or isadmin)