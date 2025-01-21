from invoke import Collection

from pre_award.account_store import tasks as account_tasks
from pre_award.assessment_store import tasks as assessment_tasks
from pre_award.common import tasks as common_tasks

namespace = Collection()
namespace.add_collection(Collection.from_module(assessment_tasks), "assessment")
namespace.add_collection(Collection.from_module(account_tasks), "account")
namespace.add_collection(Collection.from_module(common_tasks), "common")
