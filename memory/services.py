from .models import Memory

def save_memory(key,value):
    memory, created = Memory.objects.update_or_create(
        key=key,
        defaults={
            "value":value
        }
    )
    return memory

def get_memory(key):
    try:
        return Memory.objects.get(
            key=key
        )
    except Memory.DoesNotExist:
        return None

def delete_memory(key):
    Memory.objects.filter(
        key=key,
    ).delete()

def list_memories():
    return Memory.objects.all()