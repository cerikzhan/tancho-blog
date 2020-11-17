from django.contrib import messages
from django.shortcuts import render, redirect

from .models import Comment

def inactive_comments(request):
    comments = Comment.objects.inactive()

    comment_id = request.POST.get('comment_id')
    if comment_id is not None:
        try:
            comment = Comment.objects.get(id=comment_id)
        except Comment.DoesNotExist:
            messages.danger(request, 'Comment not found')
            return redirect('inactive')

        comment.is_active = True
        comment.save()
        messages.success(request, 'Comment was activated')
        return redirect('inactive')

    context = {
        'comments': comments
    }
    return render(request, 'comments/inactive_comments.html', context)

def delete_comment(request):
    comment_id = request.POST.get('comment_id')

    if comment_id is not None:
        try:
            comment = Comment.objects.get(id=comment_id)
        except Comment.DoesNotExist:
            messages.danger(request, 'Comment not found')
            return redirect('inactive')

        comment.delete()
        messages.success(request, 'Comment was deleted')
    return redirect('inactive')
    


