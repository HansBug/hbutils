hbutils.encoding.int\_hash\_val
========================================================

.. currentmodule:: hbutils.encoding.int_hash_val

.. automodule:: hbutils.encoding.int_hash_val


\_\_all\_\_
-----------------------------------------------------

.. autodata:: __all__


DeterminismValidationResult
-----------------------------------------------------

.. autoclass:: DeterminismValidationResult
    :members: passed,failed_cases,total_tested,failed_count


TypeConsistencyValidationResult
-----------------------------------------------------

.. autoclass:: TypeConsistencyValidationResult
    :members: passed,failed_cases,total_tested,failed_count,consistent_hashes


AvalancheEffectValidationResult
-----------------------------------------------------

.. autoclass:: AvalancheEffectValidationResult
    :members: passed,avg_bit_changes,change_percentage,total_comparisons,bit_changes_list,min_changes,max_changes


UniformDistributionValidationResult
-----------------------------------------------------

.. autoclass:: UniformDistributionValidationResult
    :members: passed,uniformity_score,bucket_stats,sample_count,buckets


CollisionResistanceValidationResult
-----------------------------------------------------

.. autoclass:: CollisionResistanceValidationResult
    :members: passed,collision_count,collision_rate,sample_size,unique_hashes,collision_pairs


EmptyInputValidationResult
-----------------------------------------------------

.. autoclass:: EmptyInputValidationResult
    :members: passed,hash_results,consistent_empty_hash,error_cases,empty_hash_value


PerformanceValidationResult
-----------------------------------------------------

.. autoclass:: PerformanceValidationResult
    :members: passed,performance_data,tested_sizes,completed_sizes


ComprehensiveValidationResult
-----------------------------------------------------

.. autoclass:: ComprehensiveValidationResult
    :members: __str__,passed,not_passed_properties,hash_function_name,total_properties_tested,properties_passed,determinism,type_consistency,avalanche_effect,uniform_distribution,collision_resistance,empty_input,performance


int\_hash\_val\_determinism
-----------------------------------------------------

.. autofunction:: int_hash_val_determinism


int\_hash\_val\_type\_consistency
-----------------------------------------------------

.. autofunction:: int_hash_val_type_consistency


int\_hash\_val\_avalanche\_effect
-----------------------------------------------------

.. autofunction:: int_hash_val_avalanche_effect


int\_hash\_val\_uniform\_distribution
-----------------------------------------------------

.. autofunction:: int_hash_val_uniform_distribution


int\_hash\_val\_collision\_resistance
-----------------------------------------------------

.. autofunction:: int_hash_val_collision_resistance


int\_hash\_val\_empty\_input
-----------------------------------------------------

.. autofunction:: int_hash_val_empty_input


int\_hash\_val\_performance
-----------------------------------------------------

.. autofunction:: int_hash_val_performance


int\_hash\_val\_comprehensive
-----------------------------------------------------

.. autofunction:: int_hash_val_comprehensive


