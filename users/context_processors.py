def profile_image(request):
    print("Profile image context processor called")
    if request.user.is_authenticated:
        print(f"User is authenticated: {request.user}")
        if request.user.profile_image:
            print(f"Profile image URL: {request.user.profile_image.url}")
            return {'profile_image': request.user.profile_image.url}
        else:
            print("Profile image field is empty")
    else:
        print("User is not authenticated")
    return {'profile_image': None}
