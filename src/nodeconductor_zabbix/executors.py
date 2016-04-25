from nodeconductor.core import executors, tasks


class HostCreateExecutor(executors.CreateExecutor):

    @classmethod
    def get_task_signature(cls, host, serialized_host, **kwargs):
        return tasks.BackendMethodTask().si(
            serialized_host, 'create_host', state_transition='begin_creating')


class HostUpdateExecutor(executors.UpdateExecutor):

    @classmethod
    def get_task_signature(cls, host, serialized_host, **kwargs):
        return tasks.BackendMethodTask().si(
            serialized_host, 'update_host', state_transition='begin_updating')


class HostDeleteExecutor(executors.DeleteExecutor):

    @classmethod
    def get_task_signature(cls, host, serialized_host, **kwargs):
        if host.backend_id:
            return tasks.BackendMethodTask().si(
                serialized_host, 'delete_host', state_transition='begin_deleting')
        else:
            return tasks.StateTransitionTask(serialized_host, state_transition='begin_deleting')


class ITServiceCreateExecutor(executors.CreateExecutor):

    @classmethod
    def get_task_signature(cls, itservice, serialized_itservice, **kwargs):
        return tasks.BackendMethodTask().si(
            serialized_itservice, 'create_itservice', state_transition='begin_creating')


class ITServiceDeleteExecutor(executors.DeleteExecutor):

    @classmethod
    def get_task_signature(cls, itservice, serialized_itservice, **kwargs):
        if itservice.backend_id:
            return tasks.BackendMethodTask().si(
                serialized_itservice, 'delete_itservice', state_transition='begin_deleting')
        else:
            return tasks.StateTransitionTask(serialized_itservice, state_transition='begin_deleting')


class UserCreateExecutor(executors.CreateExecutor):

    @classmethod
    def get_task_signature(cls, user, serialized_user, **kwargs):
        return tasks.BackendMethodTask().si(
            serialized_user, 'create_user', state_transition='begin_creating')


class UserUpdateExecutor(executors.UpdateExecutor):

    @classmethod
    def get_task_signature(cls, user, serialized_user, **kwargs):
        return tasks.BackendMethodTask().si(
            serialized_user, 'update_user', state_transition='begin_updating')


class UserDeleteExecutor(executors.DeleteExecutor):

    @classmethod
    def get_task_signature(cls, user, serialized_user, **kwargs):
        if user.backend_id:
            return tasks.BackendMethodTask().si(
                serialized_user, 'delete_user', state_transition='begin_deleting')
        else:
            return tasks.StateTransitionTask(serialized_user, state_transition='begin_deleting')
