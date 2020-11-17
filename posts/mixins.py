from .signals import views_signal


class ObjectViewMixin:
    def dispatch(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
        except self.model.DoesNotExist:
            instance = None

        if instance is not None:
            views_signal.send(sender=instance.__class__, instance=instance, request=request)

        return super(ObjectViewMixin, self).dispatch(request, *args, **kwargs)