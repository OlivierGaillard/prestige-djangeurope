import logging
logger = logging.getLogger('django')

class TimeSliceHelper:
    """
    It is an utility class to help filtering. It is used by the managers
    like e.g. in app "Cart" the "VenteManager".
    """

    def __init__(self, model):
        self.model = model
        self.qs = self.model.objects.all()

    def _set_year_qs(self, year):
        if self.model._meta.model_name == 'vente':
            self.qs = self.qs.filter(date__year=year)
        elif self.model._meta.model_name == 'costs':
            self.qs = self.qs.filter(billing_date__year=year)
        elif self.model._meta.model_name == 'article':
            self.qs = self.qs.filter(date_ajout__year=year)
        elif self.model._meta.model_name == 'losses':
            self.qs = self.qs.filter(date__year=year)
        else:
            raise Exception("Model {0} not handled.".format(self.model._meta.model_name))


    def _set_start_end_date_qs(self, start_date, end_date):
        if self.model._meta.model_name == 'vente':
            self.qs = self.qs.filter(date__range= (start_date, end_date))
        elif self.model._meta.model_name == 'costs':
            self.qs = self.qs.filter(billing_date__range=(start_date, end_date))
        elif self.model._meta.model_name == 'article':
            self.qs = self.qs.filter(date_ajout__range=(start_date, end_date))
        elif self.model._meta.model_name == 'losses':
            self.qs = self.qs.filter(date__range= (start_date, end_date))
        else:
            raise Exception("Model {0} not handled.".format(self.model._meta.model_name))


    def _set_start_date_qs(self, start_date):
        if self.model._meta.model_name == 'vente':
            self.qs = self.qs.filter(date__gte=start_date)
        elif self.model._meta.model_name == 'costs':
            self.qs = self.qs.filter(billing_date__gte=start_date)
        elif self.model._meta.model_name == 'article':
            self.qs = self.qs.filter(date_ajout__gte=start_date)
        elif self.model._meta.model_name == 'losses':
            self.qs = self.qs.filter(date__gte=start_date)
        else:
            raise Exception("Model {0} not handled.".format(self.model._meta.model_name))


    def _set_end_date_qs(self, end_date):
        if self.model._meta.model_name == 'vente':
            self.qs = self.qs.filter(date__lte=end_date)
        elif self.model._meta.model_name == 'costs':
            self.qs = self.qs.filter(billing_date__lte=end_date)
        elif self.model._meta.model_name == 'article':
            self.qs = self.qs.filter(date_ajout__lte=end_date)
        elif self.model._meta.model_name == 'losses':
            self.qs = self.qs.filter(date__lte=end_date)
        else:
            raise Exception("Model {0} not handled.".format(self.model._meta.model_name))


    def get_objects(self,  year=None, branch=None, start_date=None, end_date=None):
        """

        :param year:
        :param branch: if None it is a cost not bound to a specific branch. It is
        requested with a value of 'MAIN'. If the value of 'branch' is None, then
        all objects are returned (with or without a branch value).
        :param start_date:
        :param end_date:
        :return:
        """
        objects = []
        if year:
            self._set_year_qs(year)
        if start_date and end_date:
            self._set_start_end_date_qs(start_date, end_date)

        if start_date and not end_date:
            self._set_start_date_qs(start_date)

        if not start_date and end_date:
            self._set_end_date_qs(end_date)


        if branch != None and not branch == 'MAIN' :
            objects = self.qs.filter(branch=branch)
        elif branch == 'MAIN':
            objects = self.qs.filter(branch=None)
        elif branch == 'ALL':
            objects = self.qs.all()
        else:
            objects = self.qs.all()
        return objects


