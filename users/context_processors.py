def profile_image(request):
    default_image_url = "https://i.ibb.co/Ndzhyjzz/image.png"
    
    if request.user.is_authenticated:
        if request.user.profile_image:
            return {'profile_image': request.user.profile_image.url}
        else:
            return {'profile_image': default_image_url}
    else:
        return {'profile_image': default_image_url}
