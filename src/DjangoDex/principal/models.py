from django.db import models

# Create your models here.
class Pokemon(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    sprite = models.URLField(max_length=200)
    type_1 = models.CharField(max_length=50)
    type_2 = models.CharField(max_length=50, blank=True, null=True)
    
    hp = models.IntegerField()
    attack = models.IntegerField()
    defense = models.IntegerField()
    speed = models.IntegerField()
    special_attack = models.IntegerField()
    special_defense = models.IntegerField()
    
    weight = models.DecimalField(max_digits=5, decimal_places=2)
    height = models.DecimalField(max_digits=5, decimal_places=2)
    
    abilities = models.CharField(max_length=200)

    # Nuevos campos para la línea evolutiva
    evolves_from = models.ForeignKey(
        'self', 
        null=True, 
        blank=True, 
        on_delete=models.SET_NULL, 
        related_name='evolves_to'
    )

    def __str__(self):
        return self.name
    
class EvolutionLine(models.Model):
    pokemon = models.OneToOneField(Pokemon, on_delete=models.CASCADE, related_name='evolution_line')
    evolutions = models.CharField(max_length=500)  # Lista de evoluciones separadas por guiones ("Snivy - Servine - Serperior")
    sprites = models.CharField(max_length=1000, blank=True)  # URLs de los sprites separados por comas

    def __str__(self):
        return f"Línea evolutiva de {self.pokemon.name}"