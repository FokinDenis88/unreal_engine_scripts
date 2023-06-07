# TODO: Correct all class names

AssetsPrefixConventionTable = {
    ##General
    'HDRI' :                    'HDR_',
    'Material' :	            'M_',
    'MaterialInstanceConstant':	'MI_',
    'PhysicsAsset':	            'PHYS_',
    'PhysicsMaterial':	        'PM_',
    'PostProcessMaterial':      'PPM_',
    'SkeletalMesh':	            'SK_',
    'StaticMesh':	            'SM_',
    'Texture':	                'T_',
    'Texture2D':	            'T_',
    'OCIOProfile':	            'OCIO_',

    ##Blueprints
    'ActorComponent':	    'AC_',
    'AnimationBlueprint':   'ABP_',
    'BlueprintInterface':	'BI_',
    'Blueprint':	        'BP_',
    'CurveTable':	        'CT_',
    'DataTable':	        'DT_',
    'Enum':	                'E_',
    'Structure':	        'F_',
    'WidgetBlueprint':	    'WBP_',

    ##Particle Effects
    'ParticleSystem':   'PS_',
    'NiagaraEmitter':	'FXE_',
    'NiagaraSystem':	'FXS_',
    'NiagaraFunction':	'FXF_',

    ##Skeletal Mesh Animations
    'Rig':	                'Rig_',
    'Skeleton':	            'SKEL_',
    'Montages':	            'AM_',
    'Animation Sequence':   'AS_',
    'Blend Space':	        'BS_',

    ##ICVFX
    'NDisplayConfiguration':    'NDC_',

    ##Animation
    'LevelSequence':	'LS_',
    'SequencerEdits':	'EDIT_',

    ##Media
    'MediaSource':	    'MS_',
    'MediaOutput':	    'MO_',
    'MediaPlayer':	    'MP_',
    'MediaProfile':	    'MPR_',

    ##Other
    'LevelSnapshots':	    'SNAP_',
    'RemoteControlPreset':  'RCP_'
}

TextureTypesConvention = {
    ## Convention Unreal Engine Types
    'General':              ('T_', ''),
    'BaseColor':	        ('T_', '_BC'),
    'AmbientOcclusion':    ('T_', '_AO'),
    'Roughness':	        ('T_', '_R'),
    'Specular':	            ('T_', '_S'),
    'Metallic':	            ('T_', '_M'),
    'Normal':	            ('T_', '_N'),
    'Emissive':	            ('T_', '_E'),
    'Mask':	                ('T_', '_Mask'),
    'FlowMap':	            ('T_', '_F'),
    'Height':	            ('T_', '_H'),
    'Displacement':	        ('T_', '_D'),
    'LightMap':	        ('T_', '_L'),
    'Alpha/Opacity':	    ('T_', '_A'),
    'Packed':	            ('T_', '_*'),
    'TextureCube':	        ('TC_', ''),
    'MediaTexture':	    ('MT_', ''),
    'RenderTarget':	    ('RT_', ''),
    'CubeRenderTarget':	('RTC_', ''),
    'TextureLightProfile':	('TLP_', ''),
}

# https://help.poliigon.com/en/articles/1712652-what-are-the-different-texture-maps-for
# https://docs.unrealengine.com/4.27/en-US/ProductionPipelines/AssetNaming/
# https://unrealcommunity.wiki/assets-naming-convention-qqp2b5m1
# https://www.unrealdirective.com/resource/asset-naming-conventions
# https://substance3d.adobe.com/tutorials/courses/the-pbr-guide-part-2

## Maybe Upper case is not important in prefix search
# May Differ from Convention variant. Added more types.
# All checks for suffix are case insensitive
TextureTypesCustom = {
    ## General Simple Types
    #'General':              ('T_', ['']),
    'BaseColor':	        ('T_', ['', '_BC', '_BaseColor', '_Diff', '_Diffuse', '_Base_Color', '_Color', '_Base']),
    'Albedo':	            ('T_', ['_ALB', '_Albedo']),
    'AmbientOcclusion':     ('T_', ['_AO', '_AmbientOcclusion', '_Ambient', '_Occlusion', '_Occl', '_Occ', '_Occlus']),
    'Roughness':	        ('T_', ['_R', '_Roughness', '_Rough', '_Roughn']),
    'Gloss':	            ('T_', ['_G', '_Gloss', '_Glossiness'] ),
    'Specular':	            ('T_', ['_S', '_Specular', '_Spec', '_Reflection', '_Reflect', '_Refl']),
    'Metallic':	            ('T_', ['_M', '_Metallic', '_Metal']),
    'Normal':	            ('T_', ['_N', '_Normal', '_Norm']),
    'Height':	            ('T_', ['_H', '_Height']),
    'Bump':	                ('T_', ['_B', '_Bump']),
    'Displacement':	        ('T_', ['_D', '_Displacement', '_Disp', '_Displ', '_Displace', '_Displac']),
    'Emissive':	            ('T_', ['_E', '_Emissive', '_Emis', '_Emiss', '_Illumination', '_Illum', '_Illumin']),
    'Alpha/Opacity':	    ('T_', ['_A', '_Alpha', '_Opacity', '_Opac']),
    'OpacityMask':	        ('T_', ['_Mask', '_OpacMask', '_OpacityMask']),
    'LightMap':	            ('T_', ['_L', '_LightMap', '_Light']),

    ## Combo, Mix Types
    'OcclusionRoughnessMetallic':     ('T_', ['_ORM', '_RoughnessMetallic', '_RoughnMetal', '_RoughMetal',
                                               '_MetallicRoughness', '_MetalRoughn', '_MetalRough', '_MetalRoughness'
                                               '_occlusionRoughnessMetallic', '_occlusionRoughnessMetal', '_occlRoughnMetal']),
    'SpecularGlossiness':              ('T_', ['_SpecularGlossiness', '_SpecularGloss', '_SpecGloss', '_SpecGlossiness']),

    ## Unique Types
    'Convex/Concave':	    ('T_', ['_ConvexConcave', '_ConvConc', '_Convex', '_Conv', '_Concave', '_Conc']),
    'FUZZ':                 ('T_', ['_Fuzz']),

    ## Rare Types
    'FlowMap':	            ('T_', ['_F']),
    'Packed':	            ('T_', ['_*']),
    'TextureCube':	        ('TC_', ['']),
    'MediaTexture':	        ('MT_', ['']),
    'RenderTarget':	        ('RT_', ['']),
    'CubeRenderTarget':	    ('RTC_', ['']),
    'TextureLightProfile':	('TLP_', [''])

    ## By Channel
}

## Common suffix find in downloaded gltf textures files
GLTF_SuffixConvention = {
    'BaseColor':                    '_baseColor',
    'Normal':                       '_normal',
    'OcclusionRoughnessMetallic':   '_metallicRoughness',
    'Emissive':                     '_emissive'
}