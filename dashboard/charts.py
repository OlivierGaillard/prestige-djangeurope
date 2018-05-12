from jchart import Chart
from jchart.config import Axes, DataSet, rgba
from django.utils.translation import ugettext_lazy as _

class BarChart(Chart):
    chart_type = 'bar'

    purchases = 0
    costs = 0
    losses = 0
    all_costs = 0
    sellings = 0
    balance = 0


    def get_labels(self, **kwargs):
        return [_("Purchases"), _("Costs"), _("Losses"), _("All: Purch. + Costs + Losses"), _("Incomes"), _("Balance")]

    def get_datasets(self, **kwargs):

        data = [self.purchases, self.costs, self.losses, self.all_costs, self.sellings, self.balance]
        colors = [
            rgba(255, 99, 132, 0.2),
            rgba(54, 162, 235, 0.2),
            rgba(75, 192, 192, 0.2),
            rgba(153, 102, 255, 0.2),
        ]

        return [DataSet(label=_('Bar Chart'),
                        data=data,
                        borderWidth=1,
                        backgroundColor=colors,
                        borderColor=colors)]
