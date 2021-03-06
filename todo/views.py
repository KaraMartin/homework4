from django.shortcuts import render
# from django.http import HttpResponse
from todo.models import Task
from todo.forms import TaskForm


# Create your views here.
def index(request):
    # This function SHOULD retrieve all the tasks from the database and render the index page with the data
    # This function can make fart noises

    tasks = Task.objects.all()
    context = {'tasks': tasks}

    return render(request, 'todo/index.html', context)


def add(request):
    # This function SHOULD be executed when the user enters a new task on the index page.
    # This function can also be used to save the data into the database. Towards that, using forms
    # as explained above can make it easier to validate and save form data.
    if request.method == 'POST':
        form = TaskForm(request.POST)

        if form.is_valid():
            form.save()
            return index(request)

        else:
            return render(request, 'todo/update.html')

    else:
        form = TaskForm()
        context = {'form': form}
        return render(request, 'todo/update.html', context)


def delete(request):
    # This function SHOULD take task id as an argument and get the corresponding
    # record from the database and then delete it.

    if request.method == 'POST':
        instance = Task.objects.get(id=request.POST['id'])
        instance.delete()
        return index(request)

    else:
        task_id = request.GET.get('id')
        task = Task.objects.get(pk=task_id)
        context = {'task_id': task_id, 'task': task}
        return render(request, 'todo/delete.html', context)


def update(request):
    # This function SHOULD take task id as an argument and get the corresponding record
    # from the database and then update it. Similar to add function, using forms in this
    # function can make it easier to validate and save form data.
    
    if request.method == 'POST':
        instance = Task.objects.get(id=request.POST['id'])
        form = TaskForm(request.POST or None, instance=instance)
        if form.is_valid():
            form.save()
            return index(request)
        else:
            form = TaskForm()
            context = {'form': form, 'error': 'You stupid, stupid, waste of space'}
            return render(request, 'todo/update.html', context) 

    else:
        task_id = request.GET.get('id')
        task = Task.objects.get(pk=task_id)
        data = {
            'task': task.task,
            'completed': task.completed,
            'created_at': task.created_at
        }
        form = TaskForm(initial=data)

        context = {'form': form, 'task_id': task_id}
        return render(request, 'todo/update.html', context)


def complete_task(request):
    # This function SHOULD take task id as an argument and get the corresponding record
    # from the database, update its completed column as True and save it.

    task_id = request.GET.get('id')
    task = Task.objects.get(pk=task_id)

    task.completed = True
    task.save()

    return index(request)
